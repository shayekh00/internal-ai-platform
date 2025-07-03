from setuptools import setup, find_packages

setup(
    name="sixtai",
    version="0.1",
    packages=find_packages(),  # finds sixtai and its submodules
    include_package_data=True,
    install_requires=[
        "typer[all]",
        "openai",
        "langchain",
        "pyyaml",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "sixtai=sixtai.cli.main:main",  # maps CLI command to function
        ],
    },
)
