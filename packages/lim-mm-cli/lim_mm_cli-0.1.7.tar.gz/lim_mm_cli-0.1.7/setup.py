from setuptools import setup, find_packages

setup(
    name="lim-mm-cli",
    version="0.1.7",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "mm.template": ["**/*", "**/.gitkeep"]
    },
    install_requires=[
        "typer[all]",
        "jsonschema",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "lim=lim.cli:app",
            "mm=mm.cli:app",
        ]
    },
)
