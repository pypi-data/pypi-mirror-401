import subprocess
from parlancy import KubeArtifactFilePath



def kube_apply( artifact: KubeArtifactFilePath ):
    """
    kubectl apply
    TODO: ensure the artifact provided is an absolute file path or hell awaits.
    """
    if artifact.exists():
        try:
            result = subprocess.run(
                ["kubectl", "apply", "-f", path],
                check=True,
                capture_output=True,
                text=True 
            )
            return
        except subprocess.CalledProcessError as e:
            print(f"Error ({e.returncode}):\n{e.stderr}")
    raise FileNotFoundError("{path} does not exist")