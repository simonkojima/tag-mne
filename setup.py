import io
import os
import setuptools

def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("project_name", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]

setuptools.setup(
    name="tag-mne",
    version="0.0.2",
    author="Simon Kojima",
    author_email="simon.kojima@ieee.org",
    description="python library for handling tag of mne Epochs object",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/simonkojima/tag-mne",
    project_urls={
        "Bug Tracker": "https://github.com/simonkojima/tag-mne/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = read_requirements("requirments.txt"),
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)