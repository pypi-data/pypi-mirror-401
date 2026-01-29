from pathlib import Path
import tomllib
import tomli_w
from parlancy.software import PackageVersion, VersionReleaseType


def find_package_toml( path: Path ) -> Path:
    """find the absolute path to the package toml file for an argued path"""
    path = path.resolve()
    if path.is_file():
        path = path.parent
    while path != path.parent:
        toml_path = path / "pyproject.toml"
        if toml_path.exists():
            return toml_path
        path = path.parent
    raise FileNotFoundError("No pyproject.toml found in parent directories")


def bump_package_version( path: Path, type: VersionReleaseType, **kwargs, ) -> PackageVersion:
    """bump a package version (only supports semantic versioning)"""
    if not path.exists() or path.name != "pyproject.toml":
        raise ValueError("Path must point to a pyproject.toml file")

    with open(path, "rb") as f:
        data = tomllib.load(f)

    version = data.get("project", {}).get("version")
    if not version:
        raise ValueError("No version found in pyproject.toml")

    parts = version.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    match type:
        case "MAJOR":
            major += 1
            minor = 0
            patch = 0
        case "MINOR":
            minor += 1
            patch = 0
        case "PATCH":
            patch += 1

    new_version = f"{major}.{minor}.{patch}"
    data["project"]["version"] = new_version

    if kwargs.get("save", True):
        with open(path, "wb") as f:
            tomli_w.dump(data, f)

    return new_version


def get_package_version( path: Path, ) -> PackageVersion:
    """given any file or directory path inside the package, get the version of the package"""
    toml_path = find_package_toml(path)
    with open(toml_path, "rb") as f:
        data = tomllib.load(f)
    return data.get("project", {}).get("version")

def set_package_version( path: Path, version: PackageVersion, ) -> PackageVersion:
    """given any file or directory path inside the package, set the version of the package"""
    toml_path = find_package_toml(path)
    with open(toml_path, "rb") as f:
        data = tomllib.load(f)
    data["project"]["version"] = version
    with open(toml_path, "wb") as f:
        tomli_w.dump(data, f)
    return version
