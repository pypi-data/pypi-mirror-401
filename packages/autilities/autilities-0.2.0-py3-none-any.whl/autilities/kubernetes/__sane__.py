import shutil
kubectl_exists = False

def ensure_kubectl():
    global kubectl_exists
    if kubectl_exists:
        return True
    if shutil.which("kubectl") is None:
        raise EnvironmentError("kubectl is not installed or not in PATH")

ensure_kubectl()
