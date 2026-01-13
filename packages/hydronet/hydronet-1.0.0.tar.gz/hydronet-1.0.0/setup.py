from setuptools import setup, find_packages

setup(
    name="hydronet",
    version="3.0.0",
    author="Samir Baladi",
    author_email="emerladcompass@gmail.com",
    description="Hydrological Network Analysis Framework",
    packages=find_packages(where="Core_Package"),
    package_dir={"": "Core_Package"},
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scipy>=1.7.0",
        "scikit-learn>=1.0.0",
        "torch>=1.9.0",
        "networkx>=2.6.0",
        "xarray>=0.19.0",
        "flask>=2.0.0",
        "click>=8.0.0"
    ],
    python_requires=">=3.8",
)
