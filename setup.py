from setuptools import setup, find_packages

setup(
    name="intellinex-elves",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "elves=scripts.elves:cli",
        ],
    },
)