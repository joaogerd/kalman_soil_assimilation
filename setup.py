from setuptools import find_packages, setup

setup(
    name="kalman-soil-assimilation",
    version="0.1.0",
    description="Soil moisture data assimilation utilities for MONAN initial-condition development.",
    author="Joao Gerd Zell de Mattos",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "xarray",
        "netCDF4",
        "pandas",
    ],
)
