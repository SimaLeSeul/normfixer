from setuptools import setup, find_packages

setup(
    name="normfixer",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "normfixer=normfixer.cli:main"
        ]
    },
)
