import shutil
import subprocess
import sys
import tomllib
import traceback
from collections.abc import Callable
from pathlib import Path
from typing import cast


def upload_pypi(version: str):
    print("Building wheel")
    if Path("dist").is_dir():
        shutil.rmtree("dist")
    subprocess.check_call([sys.executable, "-m", "build"])

    print("Uploading release to PyPi")
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "twine",
            "upload",
            f"dist/raphson_music_headless-{version}.tar.gz",
            f"dist/raphson_music_headless-{version}-py3-none-any.whl",
        ]
    )

def retry(func: Callable[[], None]):
    while True:
        try:
            func()
            break
        except Exception:
            traceback.print_exc()
            input("Please fix then press enter to try again")
            continue


def main():
    # stdout = subprocess.check_output(["git", "status", "--porcelain"])
    # if stdout != b"":
    #     print("cannot continue, git working tree must be clean")
    #     sys.exit(1)

    projectfile = tomllib.loads(Path("pyproject.toml").read_text())
    version = cast(str, projectfile["project"]["version"])
    print("This script will make a release for version:", version)
    print(
        "You must first update CHANGES.md and pyproject.toml with the new version. Then, make a release commit with these changes."
    )
    print("Press enter to continue")
    input()

    print("Creating git tag")
    subprocess.check_call(["git", "tag", f"v{version}"])

    retry(lambda: upload_pypi(version))

    # Push tag only after everything has succeeded, so we can still fix things if the release breaks
    print("Pushing git tag")
    subprocess.check_call(["git", "push", "origin", f"v{version}"])


if __name__ == "__main__":
    main()
