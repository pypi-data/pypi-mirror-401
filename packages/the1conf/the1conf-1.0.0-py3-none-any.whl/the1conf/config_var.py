from __future__ import annotations

import copy
from collections.abc import Sequence, Callable
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import (
    Any,
    Generic,
    Optional,
    TypeAlias,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
    dataclass_transform,
    TYPE_CHECKING,
)


if TYPE_CHECKING:
    from .app_config import AppConfig


class _UndefinedSentinel:
    pass


Undefined: TypeAlias = _UndefinedSentinel
_undef: Undefined = _UndefinedSentinel()


class PathType(Enum):
    Dir = auto()
    File = auto()


__NO_SEARCH__ = "__NOSEARCH__"

_T = TypeVar("_T")


class Flags:
    """
    Flags that control how to search for variable values in AppConfig.
    These flags can be set globally in the AppConfig object or locally when calling resolve_vars() or
    per config variables.

    Not None flag values override other values with the following precedence:
        ConfigVariableDef > resolve_vars() parameters > AppConfig global flags.
    Which means that a not None value in a ConfVarDef directive will overrride a global flag value defined in AppConfig. And also that a None value in a ConfVarDef directive
    will not override the value set in resolve_vars() parameters or an AppConfig global flags.

    Attributes:
        no_env_search (bool|None): don't search values in the environment.
        no_value_search (bool|None): don't search values in the values dict.
        no_conffile_search (bool|None): don't search values in the configuration file.
        no_search (bool|None): don't search values in any location.
        click_key_conversion (bool|None): use the variable name converted to lower case and with dashes converted to underscores as
            the key to search in values.
        allow_override (bool|None): allow overriding variable in the configuration when calling resolve_vars.
        no_exception (bool|None): don't raise exception when no value is found for a variable.
    """

    _no_env_search: bool | None
    _no_value_search: bool | None
    _no_conffile_search: bool | None
    _no_search: bool | None
    _click_key_conversion: bool | None
    _allow_override: bool | None
    _no_exception: bool | None

    def __init__(
        self,
        *,
        no_env_search: Optional[bool] = None,
        no_value_search: Optional[bool] = None,
        no_conffile_search: Optional[bool] = None,
        no_search: Optional[bool] = None,
        click_key_conversion: Optional[bool] = None,
        allow_override: Optional[bool] = None,
        no_exception: Optional[bool] = None,
    ) -> None:
        self._no_env_search = no_env_search
        self._no_value_search = no_value_search
        self._no_conffile_search = no_conffile_search
        self._no_search = no_search
        if self._no_search:
            self._no_env_search = True
            self._no_value_search = True
            self._no_conffile_search = True
        self._click_key_conversion = click_key_conversion
        self._allow_override = allow_override
        self._no_exception = no_exception

    def merge(self, *, inplace: bool = False, other: Flags) -> Flags | None:
        """
        Merge the current flags with the given flags.
        If inplace is True then modify the current object, otherwise return a new Flags object.

        Flags given as parameters have precedence over the current object values if they are not None.
        """
        cur_no_search: Optional[bool]
        cur_no_env_search: Optional[bool]
        cur_no_value_search: Optional[bool]
        cur_no_conffile_search: Optional[bool]
        cur_click_key_conversion: Optional[bool]
        cur_allow_override: Optional[bool]
        cur_no_exception: Optional[bool]

        cur_no_search = (
            other._no_search if other._no_search is not None else self._no_search
        )
        if cur_no_search:
            cur_no_env_search = True
            cur_no_value_search = True
            cur_no_conffile_search = True
        else:
            cur_no_env_search = (
                other._no_env_search
                if other._no_env_search is not None
                else self._no_env_search
            )
            cur_no_value_search = (
                other._no_value_search
                if other._no_value_search is not None
                else self._no_value_search
            )
            cur_no_conffile_search = (
                other._no_conffile_search
                if other._no_conffile_search is not None
                else self._no_conffile_search
            )
        cur_click_key_conversion = (
            other._click_key_conversion
            if other._click_key_conversion is not None
            else self._click_key_conversion
        )
        cur_allow_override = (
            other._allow_override
            if other._allow_override is not None
            else self._allow_override
        )
        cur_no_exception = (
            other._no_exception if other._no_exception is not None else self._no_exception
        )
        if not inplace:
            return Flags(
                no_env_search=cur_no_env_search,
                no_value_search=cur_no_value_search,
                no_conffile_search=cur_no_conffile_search,
                no_search=cur_no_search,
                click_key_conversion=cur_click_key_conversion,
                allow_override=cur_allow_override,
                no_exception=cur_no_exception,
            )
        else:
            self._no_env_search = cur_no_env_search
            self._no_value_search = cur_no_value_search
            self._no_conffile_search = cur_no_conffile_search
            self._no_search = cur_no_search
            self._click_key_conversion = cur_click_key_conversion
            self._allow_override = cur_allow_override
            self._no_exception = cur_no_exception
            return None

    @property
    def no_env_search(self) -> bool:
        return (
            False
            if self._no_env_search is None or self._no_env_search == __NO_SEARCH__
            else self._no_env_search
        )

    @property
    def no_value_search(self) -> bool:
        return (
            False
            if self._no_value_search is None or self._no_value_search == __NO_SEARCH__
            else self._no_value_search
        )

    @property
    def no_conffile_search(self) -> bool:
        return (
            False
            if self._no_conffile_search is None
            or self._no_conffile_search == __NO_SEARCH__
            else self._no_conffile_search
        )

    @property
    def no_search(self) -> bool:
        return False if self._no_search is None else self._no_search

    @property
    def click_key_conversion(self) -> bool:
        return False if self._click_key_conversion is None else self._click_key_conversion

    @property
    def allow_override(self) -> bool:
        return False if self._allow_override is None else self._allow_override

    @property
    def no_exception(self) -> bool:
        return False if self._no_exception is None else self._no_exception


@dataclass_transform()
class ConfigVarDef(Generic[_T]):
    """
    Definition of an application configuration variable.

    Attribute of this class are called configuration directives that are used to specify the configuration of the application with the AppConfig class.

    Configuration are used indirectly by defining attributes of an AppConfig subclass with the configvar() function that creates ConfigVarDef objects:
        class MyAppConfig(AppConfig):
            my_var: int = configvar(Default=1)

    The method resolve_vars() of the AppConfig class uses these configuration variable definitions to look for the values of the variables as explained in its documentation.
    Each configuration variable definition contains several directives to define how to look for the values of the variables in a dictionnarary that can be the CLI parameters,
    or a configuration file, or an environment variables or a computation defined by a python Callable.

    Two directive are not specified in the constructor of ConfigVarDef because they are inferred from the attribute name and type hint:
        - Name : the name of the variable, inferred from the attribute name.
        - TypeInfo : the type to which to cast the variable value, inferred from the attribute type hint. Must be a python builtin type or a class or a list of
            builtin types.
            Here how to get the list of python builtin types:
                print([t.__name__ for t in __builtins__.__dict__.values() if isinstance(t, type)])
            Lists are handle with a specific processing detail below in the paragraph 'Lists'.
            Complex casting can be handle with a transfom Eval Form or with a class that implements the complex type.
            Optional value are supported like Optional[int] or Union[str, None] to indicate that the variable can be None.
            When the type hint is missing the variable is considered to be of type str.

    The directives that can be specified in configvar() are:

    - Help [optional]: a help string that describes the variable.
    - Default [optional]: the default value, can be a value or an Eval Form (see below explanation on Eval forms) whose
        returned value will be the value of the variable if no other value has been found.
        See paragraph about None below for more information.
    - EnvName [optional ]: the name of the environment variable that can contain the value. By default search for Name
    - FileKey [optional ]: the key to look for in the configuration file, key can be in the form a1.a2.a3 (attributes separated by dots) to indicate
        nested namespaces (see AppConfig documentation). By default search for Name.
    - ValueKey [optional ]: the key to look for in the "Values" dict. by default search for Name. None value are ignored.
        If the constructor parameter click_key_conversion flag (see below for flags) is true then the default value is the Name in lowercase and with '-' replaced by '_'
    - Transform : an Eval Form (see below explanation on Eval forms) that transform the value found for the variable and produce another value that will be the value
        of the variable before possible casting (like explain in TypeInfo).
    - Contexts [optional ]: a list of names indicating in which context the variable is valid. If one of the context names passed at variable resolution to
        AppConfig.resolve_vars() matches on e of the context names of the variable or if the variable has no Contexts directive then the variable is
        considered for resolution.
    - SplitToLists [optional ]: Indicates that the value found must be split in order to produce a list of string. The value
        of the directive is the list separator or True if the separator is a comma. Value in the string list will be casted to the type specified in TypeInfo.
        See the paragraph below about Lists that explain how list handled.
    - CanBeRelativeTo [optional]: a directory path or the name of another key that resolves in a directory path.
        If TypeInfo is a Path and the retrieved value is not an empty string nor None nor an absolute path then
        transform the value to an absolute path with the given directory as parent directory.
        See details below on how Path are processed.
    - MakeDirs [optional ]: a PathType that indicates the type of Path for which directories are to be created if they do not exist yet.
            if PathType is:
                - Dir : create the hierarchy of directory necessary to contains this directory as well as the directory itself
                - File: create the parent hierarchy of directory necessary to contains this file
        See details below on how Path are processed.

    - Flag directives:
        These directives can also be defined globally in the AppConfig object or when calling resolve_vars().Flags defined in a ConfigVarDef override
        the other values if they are defined.
        - NoDirProcessings [optional ]: don't run specific Path processing for this variable.
        - NoEnvSearch [optional ]: boolean, False by default. If true the value of the variable is not searched in the Environment.
        - NoValueSearch[optional ]: boolean, False by default. If true the value of the variable is not searched in the values dict.
        - NoConffileSearch [optional ]: boolean, False by default. If true the value of the variable is not searched in the configuration file.
        - ClickKeyConversion [optional ]: boolean, False by default. If true the value of the variable is converted using Click key conversion.
        - AllowOverride [optional ]: boolean, False by default. If true the variable value can be overridden by another context.
        - NoException [optional ]: boolean, False by default. If true no exception is thrown if the variable value is not found.
        - NoSearch [optional] : boolean, False by default. It true the value of the variable is not searched in the Environment, the values or the configuration
            file. It's equivaleut to set the directives NoEnvSearch, NoValueSearch, NoConffileSearch to True. In this case the value of the variable should be defined by
            the Default directive.

    For backward compatibilty the special value __NO_SEARCH__ for EnvName, ConfigKey, FileKey and ValueKey are still supported but it's recommended to use
    the NoEnvSearch, NoValueSearch, NoConffileSearch or NoSearch directives instead.

    By default throw an exception if no value are found except if no_exception is True

    Eval Forms:
    -----------

        an eval form is a callable that is evaluated to compute a value for a variable. Eval forms can be used in the Default directive or the
        Transform directive.

        The callable receives three parameters: the variable name, this configuration object and the current value found for the variable if one has been found
        in the case of a Transform directive.

        The expression can use value already defined in this application configuration object by using the first parameter of the callable which is the AppConfig object itself,
        knowing that variables are evaluated in the order they are defined.

        In the case of a Default directive the third parameter of the callable will be None.
        In the case of a Transform directive the third parameter of the callable may be None if no value have been found and
        the 'no_exception' global flag is set to True, otherwise it will be the value found for the variable before transformation.

        The returned value from the evaluation of the callable will be used to set the variable value before casting to TypeInfo.
        Note that the eventual type casting will be done after the Eval call.
        It's up to the caller to deal with the returned value.

        Note that the libraries used in Eval Forms must be imported in the module that defines the form.

        !!Warning!!: Default and Transform directives should be set or return a value that must be 'castable' to the type defined by TypeInfo.
        For example if a variable is declared as a class that accept a string in its constructor then the Default directive should be a string or an Eval
        Form that returns a string not the class instance.

    Path and Path list TypeInfo variables:
    --------------------------------------

        If a variable has a TypeInfo that is a Path or a list of Path there a dedicated processing that applies on the
        value found for them.
        This processing takes place at the end of the processing of normal variable and occurs when:
            - the TypeInfo is a Path or a list of Path
            - a value for the variable was found
            - the directive NoDirProcessing is False

        The specific processing is the following on the Path or on each of the Path in the list of Path:
            - CanBeRelativeTo: if this directive has a value that can be a path-like directory or the name of another key already defined
            that resolves in a path-like directory and the value found is not an absolute Path:
                - then make a Path with the CanBeRelativeTo directory as parent and the value found as its child.
            - MakeDirs: if this directive is True , then create the necessary directories of the path if they don't exist yet.
            - Call the 'expanduser()' and 'resolve()' method on the resulting Path.

    List:
    -----

        All values found are strings that should be casted to the type specified in TypeInfo inferred from the type hint of the variable.
        Only list of single type are supported like list[int], list[str], list[MyClass], etc.
        The value is considered as a list when SplitToList is not False and a value was found for the variable.
        In this case the temporaray string value found for the variable is split with the string 'split()' method to generate
        a list of string.
        Then all items of the list of strings are casted to the specified TypeInfo.

    Contexts:
    --------
        Every configuration variable can specify a list of context(s) in which it is valid.
        When resolving variables it is also possible to specify for which context(s) the resolution must be done.

        When one or several contexts are specify for the resolution then only the variable valid for these contexts will be considered for resolution
        as well as the VarDef without Context directive. Variable defined without Context directive are common to all context, the one with a Context directive
        are specific to their contexts.

        This allows to define variables that are specific to some context and to resolve only these variables when needed.
        When the flage AllowOverride is False and several resolutions are done, then variables are evaluated only once even if they are valid in several
        of the requested context(s), only the first valid context is used.

    None value:
    ----------
        All the VarDef valid for the involved contexts will be resolved and the one for which no value have been found will be set to None if the
        flag 'no_exception' is True.

        If the flag 'no_exception' is false and one varDef for the context has no value then an exception is raised.

        Whatever is the value of the flag 'no_exception' it is possible to set a value to None either with the 'Default' directive or with
        an Eval Form or a None value in one of the search location.

    Note on implementation:
    -----------------------
        ConfigVarDef is a descriptor class that defines the __get__ and __set__ methods.
        This allows to define configuration variables as class attributes on AppConfig subclasses.
        The __set_name__ method is used to set the Name and TypeInfo directives based on the attribute name and type hint.
    """

    _name: Optional[str] = None
    _help: str = ""
    _default: Any | Callable[[str, Any, Any], Any] | Undefined = _undef
    _env_name: Optional[str] = None
    _file_key: Optional[str] = None
    _value_key: Optional[str] = None
    _type_info: Any = None
    _transform: Optional[Callable[[str, Any, Any], Any]] = None
    _contexts: Optional[Sequence[str]] = None
    _split_to_list: Optional[bool | str | None] = None
    _can_be_relative_to: Optional[Path | str] = None
    _make_dirs: Optional[PathType] = None
    _no_dir_processing: Optional[bool] = None

    def __init__(
        self,
        *,
        Help: str = "",
        Default: Any | Callable[[str, Any, Any], Any] | Undefined = _undef,
        EnvName: Optional[str] = None,
        FileKey: Optional[str] = None,
        ValueKey: Optional[str] = None,
        Transform: Optional[Callable[[str, Any, Any], Any]] = None,
        CanBeRelativeTo: Optional[Path | str] = None,
        Contexts: Optional[Sequence[str]] = None,
        MakeDirs: Optional[PathType] = None,
        SplitToList: Optional[bool | str] = None,
        NoDirProcessing: Optional[bool] = None,
        NoSearch: Optional[bool] = None,
        NoEnvSearch: Optional[bool] = None,
        NoValueSearch: Optional[bool] = None,
        NoConffileSearch: Optional[bool] = None,
        ClickKeyConversion: Optional[bool] = None,
        AllowOverride: Optional[bool] = None,
        NoException: Optional[bool] = None,
    ) -> None:
        """Initialize the configuration variable definition.
        Should not be used directly but be used through the function configvar() to define a configuration variable as a class attribute
        on an AppConfig subclass like this:
            class MyCfg(AppConfig):
                my_var: int = configvar(Default=1)

        """
        self._help = Help
        self.__doc__ = Help
        self._default = Default
        self._env_name = EnvName
        self._file_key = FileKey
        self._value_key = ValueKey
        self._no_search = NoSearch
        self._transform = Transform
        self._can_be_relative_to = CanBeRelativeTo
        self._contexts = Contexts
        self._make_dirs = MakeDirs
        self._split_to_list = SplitToList
        self._no_dir_processing = NoDirProcessing
        self.flags = Flags(
            no_env_search=NoEnvSearch,
            no_value_search=NoValueSearch,
            no_conffile_search=NoConffileSearch,
            click_key_conversion=ClickKeyConversion,
            allow_override=AllowOverride,
            no_exception=NoException,
        )

    def __set_name__(self, owner: type, name: str) -> None:
        """This method is a special python method called when a descriptor is assigned to a class attribute.
        ConfigVarDef is a descriptor class because it defines the __get__ and __set__ methods.

        The goal of this method is to:
            - set the Name directive of this ConfigVarDef based on the attribute name.
            - infer the type of the attribute and set the TypeInfo directive with it.

        Args:
            owner (type): the owning class of the attribute that is being assigned the descriptor
            name (str): the attribute name
        """

        # set Name directive
        self._name = name

        # get all type hints of the owner class
        try:
            hints = get_type_hints(owner, include_extras=True)
        except Exception:
            hints = getattr(owner, "__annotations__", {})

        # test if there is a type hint for this attribute, if not we will consider it to be a string.
        if name in hints:
            annotated_type = hints[name]
            self._type_info = annotated_type

            if self._split_to_list is None:
                origin = get_origin(annotated_type)
                args = get_args(annotated_type)

                # Check for basic list
                if origin is list or annotated_type is list:
                    self._split_to_list = True
                # Check for Optional[list] / Union[list, ...]
                elif origin is Union:
                    for arg in args:
                        arg_origin = get_origin(arg)
                        if arg_origin is list or arg is list:
                            self._split_to_list = True
                            break
        else:
            # no type hint, consider it as a string
            self._type_info = str

    def __get__(
        self, instance: Optional[AppConfig], owner: Optional[type] = None
    ) -> ConfigVarDef[_T] | _T | None:
        """
        Descriptor method that gets the value of the configuration variable from the AppConfig instance.

        The value is retrieved from the instance's __dict__ using the variable's Name because we want to
        handle the case where we have dotted names for nested attributes.
        """
        if instance is None:
            return self
        name = self.Name
        if name in instance.__dict__:
            return instance[name]  # type: ignore
        return None

    def __set__(self, instance: AppConfig, value: Any) -> None:
        """
        Descriptor method that gets the value of the configuration variable from the AppConfig instance.
        The value is set in the instance's __dict__ using the variable's Name because we want to
        handle the case where we have dotted names for nested attributes.
        """
        instance._set_value(self.Name, value)

    @property
    def Name(self) -> str:
        if self._name is None:
            raise RuntimeError(
                "ConfigVarDef has no Name. Declare it on an AppConfig subclass "
            )
        return self._name

    @property
    def Help(self) -> str:
        return self._help

    @property
    def Contexts(self) -> Sequence[str] | None:
        return self._contexts

    @property
    def ValueKey(self) -> Optional[str]:
        """Note: we can't compute the final value here because it depends on the click_key_conversion
        flag that can be set globally or in resolve_vars."""
        if self.flags.no_value_search:
            return None
        else:
            return self.Name if self._value_key is None else self._value_key

    @property
    def EnvName(self) -> Optional[str]:
        if self.flags.no_env_search:
            return None
        else:
            return self._env_name if self._env_name is not None else self.Name

    @property
    def FileKey(self) -> Optional[str]:
        if self.flags.no_conffile_search:
            return None
        else:
            return self._file_key if self._file_key is not None else self.Name

    @property
    def Default(self) -> Any | Callable[[str, Any, Any], Any] | Undefined:
        return self._default

    @property
    def SplitToList(self) -> bool | str:
        return False if self._split_to_list is None else self._split_to_list

    @property
    def Transform(self) -> Optional[Callable[[str, Any, Any], Any]]:
        return self._transform

    @property
    def TypeInfo(self) -> Any:
        return self._type_info

    @property
    def NoDirProcessing(self) -> bool:
        return False if self._no_dir_processing is None else self._no_dir_processing

    @property
    def CanBeRelativeTo(self) -> Optional[Path | str]:
        return self._can_be_relative_to

    @property
    def MakeDirs(self) -> Optional[PathType]:
        return self._make_dirs


def configvar(
    *,
    Help: str = "",
    Default: Any | Callable[[str, Any, Any], Any] | Undefined = _undef,
    EnvName: Optional[str] = None,
    FileKey: Optional[str] = None,
    ValueKey: Optional[str] = None,
    Transform: Optional[Callable[[str, Any, Any], Any]] = None,
    CanBeRelativeTo: Optional[Path | str] = None,
    Contexts: Optional[Sequence[str]] = None,
    MakeDirs: Optional[PathType] = None,
    SplitToList: Optional[bool | str] = None,
    NoDirProcessing: Optional[bool] = None,
    NoSearch: Optional[bool] = None,
    NoEnvSearch: Optional[bool] = None,
    NoValueSearch: Optional[bool] = None,
    NoConffileSearch: Optional[bool] = None,
    ClickKeyConversion: Optional[bool] = None,
    AllowOverride: Optional[bool] = None,
    NoException: Optional[bool] = None,
) -> Any:
    """Create a declarative configuration variable definition.

    Use it as a class attribute on an AppConfig subclass:

        class MyCfg(AppConfig):
            my_var: int = configvar(Default=1)

    The variable name defaults to the attribute name and its type is inferred from the type hint of the attribute declaration.

    This function allows to assign a ConfigVarDef objects to an attribute definitions of any type by telling the type checkers
    that the type of the assignation is Any instead of ConfigVarDef.
    Indeed ConfigVarDef is a generic class and my_var: int = ConfigVarDef(...) or my_var: ConfigVarDef[int] = ConfigVarDef(...)
    would not be accepted by type checkers. configvar() declares returning Any which deactivates type checking.

    """

    return ConfigVarDef(
        Help=Help,
        Default=Default,
        EnvName=EnvName,
        FileKey=FileKey,
        ValueKey=ValueKey,
        Transform=Transform,
        CanBeRelativeTo=CanBeRelativeTo,
        Contexts=Contexts,
        MakeDirs=MakeDirs,
        SplitToList=SplitToList,
        NoDirProcessing=NoDirProcessing,
        NoSearch=NoSearch,
        NoEnvSearch=NoEnvSearch,
        NoValueSearch=NoValueSearch,
        NoConffileSearch=NoConffileSearch,
        ClickKeyConversion=ClickKeyConversion,
        AllowOverride=AllowOverride,
        NoException=NoException,
    )
