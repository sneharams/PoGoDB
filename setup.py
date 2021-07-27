import os
from pathlib import Path
from setuptools import setup, find_packages


PARENT_DIR = Path(__file__).parent
REQUIREMENTS_PATH = os.path.join(PARENT_DIR, "requirements.txt")
REQUIREMENTS_DEV_PATH = os.path.join(PARENT_DIR, "requirements-dev.txt")


with open(REQUIREMENTS_PATH) as f:
    requirements = f.read().splitlines()

with open(REQUIREMENTS_DEV_PATH) as f:
    requirements_dev = f.read().splitlines()

setup(
    name="pogodb",
    version="0.0.1",
    description="Database for analyzing Pokemon Go shop history.",
    author="Sneha Ramachandran, Joshua Anickat",
    url="https://github.com/sneharams/PoGoDB",
    packages=find_packages(),
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
