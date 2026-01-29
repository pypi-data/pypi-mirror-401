"""python functions helpful for working with the stack"""
from pathlib import Path
import inspect

def get_caller_path() -> Path:
    """get the caller of YOUR caller - the filepath which called you"""
    frame = inspect.stack()[2]
    return Path(frame.filename)
