from pathlib import Path

from setuptools import find_packages, setup


def read(path):
    return Path(path).read_text()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="{{ cookiecutter.project_slug }}",
    version=get_version("{{ cookiecutter.project_slug }}/__init__.py"),
    description="{{ cookiecutter.project_short_description }}",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.6",
    zip_safe=False,
)
