# pylint: disable=missing-module-docstring,invalid-name
from textwrap import dedent

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

with open("README.md", "r") as f:
    readme = f.read()

with open("VERSION", "r") as f:
    version = f.read().strip()

with open("src/paho_socket/version.py", "w") as f:
    f.write(
        dedent(
            """\
            # pylint: disable=missing-docstring
            __version__ = "{version}"
            """.format(
                version=version
            )
        )
    )

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
