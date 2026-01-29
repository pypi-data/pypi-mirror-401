import sys
from pathlib import Path
import importlib.util

def inject_module( module_path: Path ):
    """Lazily load a python module before it bites you in the arse..."""
    module_path = module_path / "__init__.py" if module_path.is_dir() else module_path 
    module_name = module_path.stem
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))  # build out a module-spec..
    spec.loader = importlib.util.LazyLoader(spec.loader)  # bind the loader util to it
    module = importlib.util.module_from_spec(spec) # and load it to a module
    sys.modules[module_name] = module # then jam it in the memory's model index 
    spec.loader.exec_module(module) # this puts it into a "deferred" status buecause python is a shit langugage and should be defrred... or maybe even cancelled.
    return module
