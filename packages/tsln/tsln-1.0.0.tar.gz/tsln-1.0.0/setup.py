"""Setup configuration for TSLN package."""
from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude=["tests", "benchmarks", "examples"]),
    package_data={"tsln": ["py.typed"]},
)
