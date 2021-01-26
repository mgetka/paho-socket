# pylint: disable=missing-module-docstring,invalid-name
import os.path
import sys

from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    requirements = list(
        filter(lambda line: not line.startswith("--"), f.read().splitlines())
    )

try:
    with open("requirements-dev.txt", "r") as f:
        requirements_dev = list(
            filter(lambda line: not line.startswith("--"), f.read().splitlines())
        )
except FileNotFoundError:
    requirements_dev = []

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

sys.path.insert(0, "src")
from paho_socket import __version__ as version  # pylint: disable=wrong-import-position

if "TRAVIS_TAG" in os.environ and os.environ["TRAVIS_TAG"] != version:
    print("CI release symbol differs from file defined one!")
    sys.exit(1)

setup(
    name="paho-socket",
    version=version,
    description=(
        "Thin layer built on top of paho-mqtt allowing for connections with unix socket "
        "brokers."
    ),
    long_description=readme,
    author="Michał Getka",
    author_email="michal.getka@gmail.com",
    url="https://github.com/mgetka/paho-socket",
    python_requires=">=3.7",
    include_package_data=True,
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requirements,
    keywords="paho unix",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "Operating System :: POSIX",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Communications",
        "Topic :: Internet",
    ],
    extras_require={"dev": requirements_dev},
)
