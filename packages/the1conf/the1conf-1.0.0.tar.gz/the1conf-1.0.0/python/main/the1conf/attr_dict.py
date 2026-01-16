from __future__ import annotations

from collections.abc import Mapping, MutableMapping,Sequence, Iterator
from typing import (Any, Callable, Optional,
                    Protocol, Union, get_origin)

import numpy as np
import pandas as pd

def is_sequence(obj: Any) -> bool:
    """ test if obj is a sequence (list, tuple, etc...) but not a string in thte most general way"""
    try:
        len(obj)
        obj[0:0]
        return not isinstance(obj, str)
    except KeyError:
        return False
    except TypeError:
        return False # TypeError: object is not iterable
    
class AttrDict(MutableMapping):
    """
    class which properties can be accessed like a dict or like a propertie (.x) and vis/versa:
    if used like a Dict to set a value , if the key contains dots (.) it creates a hierarchy of AttrDict object.

    Takes advantage of the internal __dict__ attribute of a class instance where are stored all the instance attributes.
    The example bellow show that we can set and read attribute with the dot notation but also through the __dict__ attribute:

    class tt:
    def __init__(self):
        self.a =2

    vt = tt()
    print(vt.__dict__)      # {'a': 2}
    vt.b = 3
    print(vt.__dict__)      #  {'a': 2, 'b': 3}
    vt.__dict__["c"] = 4
    print(vt.__dict__)      # {'a': 2, 'b': 3, 'c': 4}


    class Test(AttrDict):
    def __init__(self):
        self.var1 = "var1"
        self.__dict__["vardict"] = "vardict"
    t = Test()
    print (f"t['vardict'] = {t['vardict']}") # t['vardict'] = vardict
    print (f"t.vardict = {t.vardict}")       # t.vardict = vardict
    print (f"t['var1'] = {t['var1']}")       # t['var1'] = var1
    print (f"t.var1 = {t.var1}")             # t.var1 = var1

    t.var2 = "var2"
    print (f"t['var2'] = {t['var2']}")       # t['var2'] = var2
    print (f"t.var2 = {t.var2}")             # t.var2 = var2

    t["var3"] = "var3"
    print (f"t['var3'] = {t['var3']}")       # t['var3'] = var3
    print (f"t.var3 = {t.var3}")             #  t.var3 = var3

    t["a1.a2"] = "complexval"
    print (f"t['a1'] = {t['a1']}")           # t['a1'] = {'a2': 'complexval'}
    print (f"t.a1 = {t.a1}")                 # t.a1 = {'a2': 'complexval'}
    """

    def __init__(self, init: Optional[Mapping[Any, Any]] = None) -> None:
        if init is not None:
            self.__dict__.update(init)

    def __contains__(self, key: Any) -> bool:
        try:
            eval(f"self['{key}']")
        except Exception:
            return False
        return True

    def __getitem__(self, key: Any) -> Any:
        """
        Called to implement evaluation of self[key]
        attributes with dots in their name are read in sub AttrDict Objects.
        """
        if isinstance(key, slice):
            raise KeyError("slices are not supported")
        parts = key.split(".")
        curpart = parts[0]

        if len(curpart.strip()) == 0:
            raise AttributeError(f"bad attribute name: {key}")
        elif len(parts) > 1:
            if curpart in self.__dict__:
                sub_attr = self.__dict__[curpart]
            else:
                raise AttributeError(f"key {curpart} not set")
            return sub_attr[".".join(parts[1:])]
        else:
            return self.__dict__[curpart]

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Called to implement assignment to self[key].
        attributes with dots in their name are put in sub AttrDict Objects.
        """
        if isinstance(key, slice):
            raise KeyError("slices are not supported")
        parts = key.split(".")
        curpart = parts[0]

        if len(curpart.strip()) == 0:
            raise AttributeError(f"bad attribute name: {key}")
        elif len(parts) > 1:
            if curpart in self.__dict__:
                sub_attr = self.__dict__[curpart]
            else:
                sub_attr = AttrDict()
                self.__dict__[curpart] = sub_attr
            sub_attr[".".join(parts[1:])] = value
        else:
            self.__dict__[curpart] = value

    def __delitem__(self, key: Any) -> None:
        """Called to implement deletion of self[key]."""
        del self.__dict__[key]

    def __len__(self) -> int:
        """Called to implement the built-in function len()"""
        return len(self.__dict__)

    def __iter__(self) -> Iterator:
        """This method is called when an iterator is required for a container."""
        return self.__dict__.__iter__()

    def update(  # type: ignore
        self, other: Mapping[Any, Any], override: bool = False
    ) -> None:
        if override:
            res = self.__dict__ | other  # type: ignore
        else:
            res = other | self.__dict__  # type: ignore
        self.__dict__ = res

    def _repr_with_ident(self, indent: int) -> list[str]:
        res = []
        indent_str = "\t" * indent
        for n, v in self.__dict__.items():
            if issubclass(self.__class__, type(v)):
                res.append(f"{indent_str}{n} :")
                res.extend(v._repr_with_ident(indent + 1))
            else:
                res.append("{}{} : {}".format(indent_str, n, v))
        return res

    def __repr__(self) -> str:
        res = self._repr_with_ident(0)
        return "\n".join(res)

    def clone(self) -> AttrDict:
        return AttrDict(self.__dict__)
