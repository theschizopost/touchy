from setuptools import setup, find_packages

setup(
    name="touchy",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "touchy=src.cli:main",
        ],
    },
    install_requires=[],
    python_requires=">=3.6"
)