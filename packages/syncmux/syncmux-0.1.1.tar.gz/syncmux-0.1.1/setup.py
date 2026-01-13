#!/usr/bin/env python3
from setuptools import setup, find_packages
from pathlib import Path

version = {}
with open("syncmux/version.py") as f:
    exec(f.read(), version)

readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="syncmux",
    version=version['__version__'],
    description="Fast file synchronization for remote development over SSH",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Shantanu Banerjee",
    author_email="shantanu@banerg.net",
    url="https://github.com/bradley101/syncmux",
    license="MIT",
    packages=find_packages(),
    install_requires=["watchdog>=3.0.0"],
    entry_points={'console_scripts': ['syncmux=syncmux.cli:main']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    keywords="ssh sync development remote rsync",
)
