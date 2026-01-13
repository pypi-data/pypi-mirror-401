from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="pyodbc-extras",
    packages=["pyodbc_extras"],
    package_dir={"pyodbc_extras": "pyodbc_extras"},
    package_data={
        "pyodbc_extras": [
            "__init__.py",
        ]
    },
    version="0.0.0",
    description="Extra Methods for Working with ODBC Connections in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel J. Dufour",
    author_email="daniel.j.dufour@gmail.com",
    url="https://github.com/DanielJDufour/pyodbc-extras",
    download_url="https://github.com/DanielJDufour/pyodbc-extras/tarball/download",
    keywords=["data", "odbc", "python", "sql"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
)
