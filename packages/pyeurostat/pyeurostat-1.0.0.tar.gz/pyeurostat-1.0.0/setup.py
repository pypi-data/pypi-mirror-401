from setuptools import setup, find_packages

setup(
    name="pyeurostat",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "plotly>=5.0.0",
        "requests>=2.25.0",
    ],
)
