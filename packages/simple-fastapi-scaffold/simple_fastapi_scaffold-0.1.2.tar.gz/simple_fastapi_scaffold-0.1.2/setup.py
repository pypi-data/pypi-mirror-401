from setuptools import setup, find_packages

setup(
    name="simple_fastapi_scaffold",
    version="0.1.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "click>=8.1.0",
        "jinja2>=3.1.0",
        "pydantic>=2.0.0",
        "rich>=13.0.0",
        "toml>=0.10.0",
    ],
    entry_points={
        "console_scripts": [
            "simple-fastapi-scaffold=fastapi_scaffold.cli:main",
            "fasc=fastapi_scaffold.cli:main",
        ],
    },
)
