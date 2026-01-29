from autilities.pythonic import get_caller_path

def log(message: str, ):
    caller = get_caller_path()
    target = caller.parent / "trace.log"
    print("TTTTTTTTTTTTTTTTt", target)
    target.write_text(message, encoding="utf8")
