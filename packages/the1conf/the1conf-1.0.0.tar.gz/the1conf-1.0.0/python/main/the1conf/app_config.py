from __future__ import annotations

import dataclasses
import importlib
import json
import logging
import copy
import os
import ast
import inspect
import textwrap
from collections.abc import Iterable, Mapping, MutableMapping, Sequence
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import (
    Annotated,
    Any,
    Callable,
    cast,
    Generic,
    Optional,
    TypeAlias,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
    dataclass_transform,
)

import yaml

from .attr_dict import AttrDict, is_sequence
from pydantic import TypeAdapter, ValidationError
from .config_var import ConfigVarDef, Flags, PathType, Undefined, _UndefinedSentinel, _undef, configvar


def _get_attribute_docstrings(cls: type) -> dict[str, str]:
    """
    Extracts docstrings for class attributes by parsing the source code.
    This allows using docstrings to populate ConfigVarDef.Help.
    """
    docstrings = {}
    try:
        source = inspect.getsource(cls)
        # Deduct to handle nested classes indentation
        source = textwrap.dedent(source)
    except (OSError, TypeError):
        # Source code not available (e.g. dynamic class, REPL, compiled files)
        return {}

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {}

    # We look for the ClassDef in the parsed source.
    # Since inspect.getsource(cls) returns the class definition itself,
    # the first node in body should be the ClassDef.
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for i, item in enumerate(node.body):
                if isinstance(item, (ast.Assign, ast.AnnAssign)):
                    # Check if the next node is an expression containing a string (docstring)
                    if i + 1 < len(node.body):
                        next_node = node.body[i + 1]
                        if (
                            isinstance(next_node, ast.Expr)
                            and isinstance(next_node.value, ast.Constant)
                            and isinstance(next_node.value.value, str)
                        ):
                            docstring = next_node.value.value.strip()

                            targets = []
                            if isinstance(item, ast.Assign):
                                targets = item.targets
                            elif isinstance(item, ast.AnnAssign):
                                targets = [item.target]

                            for target in targets:
                                if isinstance(target, ast.Name):
                                    docstrings[target.id] = docstring
            # We found the class def, no need to continue in top level
            break
            
    return docstrings


class AppConfigException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NameSpace:
    """Marker class for configuration namespaces.
    Used to group configuration variables into nested namespaces within an AppConfig subclass.
    See AppConfig documentation for more information.
    """

    pass


class AppConfig(AttrDict):
    """ "
    A class to manage application configuration. It can be passed from callable to callable.
    It can search for variable values in command line arguments, environment variables, a yaml or json configuration file
    or a default value or a computed value.

    Configuration variable are defined with a list of ConfigVarDef object which defines how to look for the variable values and/or compute them.

    The variable values are searched in these locations in the following order:
    - a dict of values usually passed from the command line arguments
    - environment variables
    - a configuration file in yaml or json format
    - a default value or a computed value
    The first match found is used as the value for the variable.

    When found the variable can be casted to a specific type and/or transformed with a callable.

    The default value can also be computed with a callable that can use already defined variables in this AppConfig object.
    One can combine a default value and a transformation callable to compute complex default values that can combine several already defined variables,
    knowing that variables are resolved in the order they are declared in the AppConfig subclass.

    See method 'resolve_vars()' and class 'ConfigVarDef' for more information.

    Variable can also be set directly like in an object attribute or in a Dict key:

    ctx = AppConfig()
    ctx["var"] = 2
    print(ct.var) # print 2

    Accessing the variables can also be done like an object attribute or a Dict key:
    ctx = AppConfig()
    ctx.var = 2
    print(ctx["var"]) # print 2

    This can be useful to mix known variable name and variable dynamically defined in a file or passed from the command line.
    def foo(ctx: AppConfig,attname:Any) -> Any:
        return ctx[attname]

    Variable can contain variable recursively, in this case they can be access with a dotted notation or with a dict like way:
    ctx = AppConfig()
    ctx["var1.var2"] = 2
    ctx["var1.var3"] = 3
    print(f"var1 = {ctx.var1}") # print a dict {"var2":2,"var3":3}

    print(ctx.var1.var2) # print 2

    Declarative Configuration:
    --------------------------
    Configuration is best defined declaratively by subclassing AppConfig:

        class MyConfig(AppConfig):
            host: str = configvar(Default="localhost")
            port: int = configvar(Default=8080)

    Nested Namespaces:
    ------------------
    Variables can be grouped into namespaces using nested classes inheriting from NameSpace.
    This creates a structured configuration:

        class MyConfig(AppConfig):
            # Root level variable
            debug: bool = configvar(Default=False)

            # Nested namespace 'db'
            class db(NameSpace):
                host: str = configvar(Default="db.local")
                port: int = configvar(Default=5432)

            # Nested namespace 'api'
            class api(NameSpace):
                key: str = configvar(EnvName="API_KEY")

    inst = MyConfig()
    inst.resolve_vars()
    print(inst.db.host)  # Access nested variables

    Decentralized Configuration (Mixins):
    -------------------------------------
    Configuration can be split across multiple classes (Mixins) and combined using inheritance.
    This allows different modules to define their own configuration requirements.

        class DatabaseConfig(AppConfig):
            class db(NameSpace):
                host: str = configvar(Default="localhost")

        class ApiConfig(AppConfig):
            class api(NameSpace):
                timeout: int = configvar(Default=30)

        # Combine into the final application config
        class App(DatabaseConfig, ApiConfig):
            pass

    If multiple mixins define the same namespace (e.g. `class db(NameSpace)`), their variables are merged.
    """

    #: The logger for this class
    _logger = logging.getLogger(__name__)
    _solver_logger = logging.getLogger(f"{__name__}.solver")
    _global_flags: Flags
    _config_var_defs: list[ConfigVarDef]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Call when a subclass inherits from AppConfig.

        Create the _config_var_defs attribute that contains the list of ConfigVarDef
        defined in this subclass as well as the ones defined in parent classes.
        """
        super().__init_subclass__(**kwargs)

        # First try to look if there is already a _config_var_defs attribute in one of the parent classes.
        collected: list[ConfigVarDef] = []
        seen_attr_names: set[str] = set()
        for base in reversed(cls.__mro__[1:]):
            # from the deepest parent class to the nearest parent class: search if there
            # is a _config_var_defs attribute in the inspected class.
            base_defs = getattr(base, "_config_var_defs", None)
            if not base_defs:
                continue
            for var_def in base_defs:
                # base_defs is the _config_var_defs list. Loops on each of its elements and store them in the collected list
                # For each one read its name. If the variable name is already in the collected list, it means that it has been
                # defined in a parent class of the current inspected base class. So we remove the old definition and add the new one.
                attr_name = getattr(var_def, "_name", None)
                if attr_name:
                    if attr_name in seen_attr_names:
                        collected = [
                            v for v in collected if getattr(v, "_name", None) != attr_name
                        ]
                    collected.append(var_def)
                    seen_attr_names.add(attr_name)

        # Helper method for recursive collection
        def collect_vars(owner: type, prefix: str = "") -> Iterable[ConfigVarDef]:
            # extract docstrings from the class source code
            docstrings = _get_attribute_docstrings(owner)

            # Inspect the class __dict__ to find ConfigVarDef defined in this class
            for attr_name, value in owner.__dict__.items():
                if isinstance(value, ConfigVarDef):
                    # Clone to update name with prefix
                    # We use copy.copy because ConfigVarDef is mutable but generic.
                    new_var = copy.copy(value)
                    
                    # If Help is missing, try to use the docstring
                    if not new_var.Help and attr_name in docstrings:
                        new_var._help = docstrings[attr_name]

                    if prefix:
                        # We need to access _name directly
                        original_name = getattr(value, "_name", attr_name)
                        new_var._name = f"{prefix}{original_name}"

                    yield new_var

                elif (
                    isinstance(value, type)
                    and issubclass(value, NameSpace)
                    and value is not NameSpace
                ):
                    # Recurse
                    yield from collect_vars(value, prefix=f"{prefix}{attr_name}.")

        # Now inspect the class __dict__ to find ConfigVarDef defined in this class (and nested classes) and add them to the collected list.
        for value in collect_vars(cls):
            attr_name = getattr(value, "_name", None)
            if attr_name:
                if attr_name in seen_attr_names:
                    collected = [
                        v for v in collected if getattr(v, "_name", None) != attr_name
                    ]
                collected.append(value)
                seen_attr_names.add(attr_name)

        cls._config_var_defs = collected

    def __init__(
        self,
        *,
        no_env_search: Optional[bool] = None,
        no_key_search: Optional[bool] = None,
        no_conffile_search: Optional[bool] = None,
        no_search: Optional[bool] = None,
        conffile_path: Optional[Path] = None,
        allow_override: Optional[bool] = None,
        click_key_conversion: Optional[bool] = None,
    ):
        """Init the config.

        Arguments are called 'global flags', they specify the behavior of the variable resolution globaly. They can be overiden
        when the resolve method is call. (this method can be call several time and thus on each call some flags can be changed) or
        per variable when defining the ConfigVarDef object.

        Global Flags:
            no_env_search (bool, optional): don't search values in the environment. Defaults to False.
            no_key_search (bool, optional): don't search values in the value dictionary. Defaults to False.
            no_conffile_search (bool, optional): don't search values in the configuration file. Defaults to False.
            no_search (bool, optional): don't search values in any location. Defaults to False.
            conffile_path (Path, optional): the configuration file path. Defaults to None.
            allow_override (bool, optional): allow overriding variable in the configuration when calling resolve_vars.
                it happens either when resolve_vars() is call several times or the variable was set before its call.
            click_key_conversion (bool, optional): use the variable name converted to lower case and with dashes converted to underscores as
            the key to search in values. Defaults to False.
        """
        self._global_flags = Flags(
            no_env_search=no_env_search,
            no_value_search=no_key_search,
            no_conffile_search=no_conffile_search,
            no_search=no_search,
            click_key_conversion=click_key_conversion,
            allow_override=allow_override,
        )
        self.conffile_path = conffile_path
        # Configuration variable definitions used by resolve_vars().
        # This is intentionally an instance attribute so callers can set/replace it
        # dynamically (major-version breaking change: resolve_vars no longer accepts
        # a var_specs parameter).
        # Default to the declarative definitions collected on the class.
        self._config_var_defs = list(getattr(self.__class__, "_config_var_defs", []))
        self._logger.debug("init AppCtx")

    def clone(self) -> AppConfig:
        """cloning the AppConfig object"""
        clone = AppConfig()
        clone.__dict__ = self.__dict__.copy()
        return clone

    @classmethod
    def _find_var_in_dict(cls, where: Mapping[Any, Any], var_name: str) -> Any | Undefined:
        """
        Search for var_name in a dictionary.
        var_name contains dict keys separated by a dot (.) ie key1.key2.key3
        The left side key key1 is search in the where directory, if it is found
        and it is a dictionary then key2 is search in it and
        all key are searched in sequence.
        Returns _undef if not found, allowing to distinguish between None (explicit null) and missing.
        """
        cur_dic: Mapping[Any, Any] = where
        for key in var_name.split("."):
            # logger = logging.getLogger(f"{cls.__module__}.{cls.__name__}")
            # logger.debug(f"searching for key: {key} in dict : {cur_val}")
            if key in cur_dic:
                cur_dic = cur_dic[key]
                # logger.debug(f"Found key: {key} = {cur_val}")
            else:
                return _undef

        return cur_dic

    def _run_eval(
        self,
        callable: Callable[[str, Any, Any], Any],
        var_val: Any = None,
        var_name: str = "",
    ) -> Any:
        """
        Call a Callable found in a Eval Form.
        """
        return callable(var_name, self, var_val)

    def _set_value(self, name: str, value: Any) -> None:
        """Set a value.

        Depending on AttrDict implementation to handle dotted keys and not trigger recursion loops
        if called from a descriptor.
        """
        self[name] = value

    def resolve_vars(
        self,
        *,
        contexts: Optional[str | Iterable[str]] = None,
        values: Mapping[str, Any] = {},
        no_exception: Optional[bool] = None,
        no_env_search: Optional[bool] = None,
        no_value_search: Optional[bool] = None,
        no_conffile_search: Optional[bool] = None,
        no_search: Optional[bool] = None,
        conffile_path: Optional[Path] = None,
        allow_override: Optional[bool] = None,
        click_key_conversion: Optional[bool] = None,
    ) -> Any:
        """
        Resolve the configuration variables defined in this AppConfig object.
        The variable values are searched in these locations in the following order:
        - a dict of values usually passed from the command line arguments
        - environment variables
        - a configuration file in yaml or json format
        - a default value or a computed value
        The first match found is used as the value for the variable.
        When found the variable can be casted to a specific type and/or transformed with a callable.
        The default value can also be computed with a callable that can use already defined variables in this AppConfig object.
        One can combine a default value and a transformation callable to compute complex default values that can combine several already defined variables,
        knowing that variables are resolved in the order they are declared in the AppConfig subclass.
        """

        self._logger.info(
            f"Starting variable resolution, conf file = {str(conffile_path)}  "
        )

        # Compute flags that can be override locally.
        resolve_flags = Flags(
            no_env_search=no_env_search,
            no_value_search=no_value_search,
            no_conffile_search=no_conffile_search,
            no_search=no_search,
            click_key_conversion=click_key_conversion,
            allow_override=allow_override,
            no_exception=no_exception,
        )
        local_flags = self._global_flags.merge(inplace=False, other=resolve_flags)
        assert local_flags is not None

        # Read configuration file if requiered
        conf_file_vars = None
        cur_conffile_path = conffile_path if conffile_path else self.conffile_path
        if not local_flags.no_conffile_search and cur_conffile_path is not None:
            if cur_conffile_path.is_file():
                with cur_conffile_path.open("r") as f:
                    if cur_conffile_path.suffix.lower() == ".json":
                        self._logger.debug(f"Parsing json file {cur_conffile_path}")
                        conf_file_vars = json.load(f)
                    else:
                        self._logger.debug(
                            f"Parsing file {cur_conffile_path} with suffix {cur_conffile_path.suffix.lower()}"
                        )
                        conf_file_vars = yaml.safe_load(f)
            else:
                self._logger.info(f"configuration file {cur_conffile_path} not found.")

        # Read the var definitions one by one in their definition order
        for var in self._config_var_defs:
            # compute the current flags for this variable by merging local flags with variable flags
            cur_flags = local_flags.merge(inplace=False, other=var.flags)
            assert cur_flags is not None
            # self.logger.debug(f"looking for a value for variable: {var.Name}")

            self._solver_logger.debug(f"Searching for var name {var.Name}:\n{str(var)}")

            # if we are resolving the variables in some specific contexts (ie parameter context has value)
            # we check if the variable belongs to one of these contexts and if not we skip it.
            if contexts is None and var.Contexts is not None:
                continue
            if contexts is not None and var.Contexts is not None:
                test_ctx = []
                # put True in test_ctx for each context that matches, False otherwise
                if is_sequence(contexts):
                    test_ctx = [c in var.Contexts for c in contexts]
                else:
                    test_ctx = [contexts in var.Contexts]

                # test if there is any True in test_ctx which means that at least one context matches
                if not any(test_ctx):
                    continue

            if var.Contexts is None and contexts is not None:
                # variable without context are common to all contexts so we process them but only once.
                if var.Name in self.__dict__:
                    continue

            # if the variable is already defined and override is not allowed then
            # we skip it (First valid context wins).
            if not cur_flags.allow_override and var.Name in self.__dict__:
                continue

            val_found: str | None | list[Any] | Undefined = _undef
            found = False

            #  Searching variable value in the values mapping
            if (
                values is not None
                and not cur_flags.no_value_search
                and var.ValueKey is not None
            ):
                # searching var key
                if var.ValueKey in values and values[var.ValueKey] is not None:
                    val_found = values[var.ValueKey]
                    found = True
                    self._solver_logger.debug(
                        f"{var.Name} -> Found in Values = {val_found}"
                    )
                if not found and cur_flags.click_key_conversion:
                    # try with click key conversion
                    click_key = var.ValueKey.lower().replace("-", "_")
                    if click_key in values and values[click_key] is not None:
                        val_found = values[click_key]
                        found = True
                        self._solver_logger.debug(
                            f"{var.Name} -> Found in Values with Click Key Conversion = {val_found}"
                        )
            # Searching variable value in the environment variables
            if not found and not cur_flags.no_env_search and var.EnvName is not None:
                env_val = os.getenv(var.EnvName)
                if env_val is not None:
                    val_found = env_val
                    found = True
                    self._solver_logger.debug(f"{var.Name} -> Found in Env = {val_found}")
            #  Searching variable value in the configuration file
            if (
                not found
                and not cur_flags.no_conffile_search
                and conf_file_vars is not None
                and var.FileKey is not None
            ):
                file_val = self._find_var_in_dict(conf_file_vars, var.FileKey)
                if file_val is not _undef:
                    val_found = file_val
                    found = True
                    self._solver_logger.debug(
                        f"{var.Name} -> Found in Configuration File = {val_found}"
                    )
            #  Setting variable value to the default value if defined.
            if not found and var.Default is not _undef:
                if var.Default is not None and callable(var.Default):
                    val_found = self._run_eval(callable=var.Default, var_name=var.Name)
                else:
                    val_found = var.Default
                found = True
                self._solver_logger.debug(
                    f"{var.Name} -> Found in Default Value = {val_found}"
                )

            # Raise exception if no value was found and no_exception is True
            if not found and not cur_flags.no_exception:
                raise AppConfigException(
                    f"No value for var {var.Name} in context {contexts}"
                )

            if found:
                if isinstance(val_found, _UndefinedSentinel):
                    raise AssertionError(
                        "Internal error: val_found is _undef while found=True"
                    )
                # spliting lists
                if (
                    var.SplitToList
                    and val_found is not None
                    and isinstance(val_found, str)
                ):
                    sep: str = (
                        "," if isinstance(var.SplitToList, bool) else var.SplitToList
                    )
                    val_found = val_found.split(sep)

                # Transform the variable value if specified.
                if var.Transform is not None:
                    val_transfo = self._run_eval(
                        callable=var.Transform,
                        var_val=val_found,
                        var_name=var.Name,
                    )
                    self._solver_logger.debug(
                        f"{var.Name} -> Value Transformed: {val_found} => {val_transfo}"
                    )
                    val_found = val_transfo

                # Validate and cast the variable value using pydantic TypeAdapter
                if var.TypeInfo is not None and val_found is not None:
                    try:
                        ta = TypeAdapter(var.TypeInfo)
                        val_found = ta.validate_python(val_found)
                    except ValidationError as e:
                        raise AppConfigException(f"Validation failed for var {var.Name}: {e}")

                self._set_value(var.Name, val_found)
            elif var.Name not in self.__dict__:
                # in case of overiding and when on subsenquent call no value were found we don't want to erase a value
                # found on a previous run. This can happen when some global flags are overriden or for variable without
                # context.
                self._set_value(var.Name, None)

            # Make special treatment for paths
            if (
                not var.NoDirProcessing
                and var.TypeInfo == Path
                and self[var.Name] != None
            ):
                var_value = self[var.Name]
                new_val: list[Path] | Path | None = None
                try:
                    if iter(var_value):
                        # we need to consider the case where the variable is a list of Path
                        new_val = []
                        for val in var_value:
                            res = self._process_paths(value=val, var=var)
                            new_val.append(res)
                except Exception:
                    res = self._process_paths(value=var_value, var=var)
                    new_val = res
                self._set_value(var.Name, new_val)

    def _process_paths(self, *, value: Any, var: ConfigVarDef) -> Path:
        """
        Run the path processing for a single Path variable.
        
        """ 

        var_value: Path
        if isinstance(value, str):
            var_value = Path(value)
        elif isinstance(value, Path):
            var_value = value
        else:
            raise Exception("not a path")

        res: Path = var_value
        # First process the CanBeRelative case.
        if var.CanBeRelativeTo is not None:

            if var_value.is_absolute():
                res = var_value
            else:
                # resolving the root directory from which to be relative to.
                can_be_relative = var.CanBeRelativeTo
                root_dir: Path
                if isinstance(can_be_relative, str) and can_be_relative in self.__dict__:
                    root_dir = Path(self[can_be_relative])
                else:
                    root_dir = Path(can_be_relative)
                res = root_dir.joinpath(var_value)

        # Expanding user home and resolving dots in path
        res = res.expanduser().resolve()

        # create directory if MakeDir is not None
        if var.MakeDirs:
            if var.MakeDirs == PathType.Dir:
                res.mkdir(parents=True, exist_ok=True)
            else:
                res.parent.mkdir(parents=True, exist_ok=True)
        return res

    def __repr__(self) -> str:
        mess = ["App Context:"]
        for cur_var, cur_val in self.__dict__.items():
            mess.append(f"\t{cur_var}:\t{cur_val}")

        return "\n".join(mess)
