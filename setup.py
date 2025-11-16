from setuptools import setup, find_packages

setup(
    name="aon",
    version="1.0.0",
    packages=find_packages(),
    description="AON — Artificial Object Notation (binding Python via ctypes)",
    author="Mateus Henrique",
    python_requires=">=3.8",
    include_package_data=True,
)
