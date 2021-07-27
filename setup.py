import os
from setuptools import setup, find_packages


PARENT_DIR = os.path.abspath(os.path.dirname(__file__))
REQUIREMENTS_PATH = os.path.join(PARENT_DIR, "requirements.txt")
REQUIREMENTS_DEV_PATH = os.path.join(PARENT_DIR, "requirements-dev.txt")
README_PATH = os.path.join(PARENT_DIR, "README.md")


with open(REQUIREMENTS_PATH) as f:
    requirements = f.read().splitlines()

with open(REQUIREMENTS_DEV_PATH) as f:
    requirements_dev = f.read().splitlines()

with open(README_PATH, encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pogodb",
    version="0.0.1",
    description="Database for analyzing Pokemon Go shop history.",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
