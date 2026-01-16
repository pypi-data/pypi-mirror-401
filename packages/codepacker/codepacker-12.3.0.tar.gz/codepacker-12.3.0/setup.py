from setuptools import setup, find_packages

setup(
    name="codepacker",
    version="12.3.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "codepacker=codepacker.GUI:start",
        ],
    },
)
