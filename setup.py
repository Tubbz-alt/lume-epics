from setuptools import setup, find_packages
from os import path, environ

cur_dir = path.abspath(path.dirname(__file__))

# parse requirements
with open(path.join(cur_dir, "requirements.txt"), "r") as f:
    requirements = f.read().split()

# set up additional dev requirements
dev_requirements = []
with open(path.join(cur_dir, "dev-requirements.txt"), "r") as f:
    dev_requirements = f.read().split()

setup(
    name="lume-epics",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
    # set up development requirements
    extras_require={"dev": dev_requirements},
    url="https://github.com/slaclab/lume-epics",
    include_package_data=True,
    python_requires=">=3.7",
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest'],
)
