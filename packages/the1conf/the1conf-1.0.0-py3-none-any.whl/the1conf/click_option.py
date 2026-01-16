from __future__ import annotations
from typing import Any, Callable

import click

from .app_config import ConfigVarDef, Undefined

def click_option(config_var: Any, **kwargs: Any) -> Callable[[Any], Any]:
    """Wrappe click.option avec les métadonnées de ConfigVarDef."""
    if not isinstance(config_var, ConfigVarDef):
        raise TypeError(f"click_option expects a ConfigVarDef, got {type(config_var)}")
        
    
    # 1. Nom du flag (ex: my_var -> --my-var)
    param_name = config_var.Name
    flag_name = f"--{param_name.replace('_', '-').lower()}"
    
    # 2. Documentation
    if "help" not in kwargs and config_var.Help:
        kwargs["help"] = config_var.Help

    # 3. Contrainte stricte : Toujours des strings
    # On écrase tout type passé pour garantir que resolve_vars reçoive du string.
    kwargs["type"] = click.STRING
    
    # 4. Affichage du défaut sans l'appliquer
    if "show_default" not in kwargs and config_var.Default is not Undefined and not callable(config_var.Default):
        # On doit convertir en string sinon click interprete les bool/int comme des flags (True/False)
        # qui lui disent "affiche le default" (qui est None ici), du coup il n'affiche rien.
        kwargs["show_default"] = str(config_var.Default)

    # Note: On ne passe PAS 'envvar' ni 'default'
    
    # On force le nom de destination pour qu'il matche la clé attendue par the1conf
    return click.option(flag_name, param_name, **kwargs)
