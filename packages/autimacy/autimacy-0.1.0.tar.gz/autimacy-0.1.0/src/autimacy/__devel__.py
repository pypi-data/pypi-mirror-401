from pathlib import Path
from os import environ, chdir
from autilities.shell import run
from shutil import rmtree

def watch():
    from autilities.testing import watch as watcher
    pkg_root = Path(__file__).parent.parent.parent
    watcher(root=pkg_root)


def publish():
    API_KEY = environ.get("PYPI_API_KEY")
    if API_KEY:
        pkg_path = Path(__file__).parent.parent.parent
        dist_path = pkg_path / "dist"
        if dist_path.exists():
            rmtree(dist_path)
        chdir(pkg_path)
        run("uv build --out-dir ./dist")

        uenv = environ.copy()
        uenv["TWINE_USERNAME"] = "__token__"
        uenv["TWINE_PASSWORD"] = API_KEY

        print(f"twine upload commencing...")
        run("python -m twine upload dist/*", env=uenv)
        print(f"twine upload was successful")
        return
    raise EnvironmentError("cannot publish -- missing PYPI_API_KEY")
