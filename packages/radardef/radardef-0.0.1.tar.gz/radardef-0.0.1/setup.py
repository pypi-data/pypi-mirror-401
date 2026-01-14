import codecs
import pathlib

import setuptools

HERE = pathlib.Path(__file__).resolve().parents[0]


def get_version(path):
    with codecs.open(path, "r") as fp:
        for line in fp.read().splitlines():
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
        else:
            raise RuntimeError("Unable to find version string.")


setuptools.setup(
    version=get_version(HERE / "src" / "radardef" / "version.py"),
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": ["*.ini", "*.txt", "*.npz", "*.npy", "antpos.csv*"]},
    include_package_data=True,
)
