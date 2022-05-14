import pathlib

from setuptools import setup

PACKAGE = "roboswag"
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
with open(HERE / PACKAGE / "version.py") as f:
    __version__ = f.read().split("=")[1].strip().strip('"')
CLASSIFIERS = """
Development Status :: 3 - Alpha
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Framework :: Robot Framework
Framework :: Robot Framework :: Tool
Topic :: Software Development :: Testing
Topic :: Software Development :: Quality Assurance
Topic :: Utilities
Intended Audience :: Developers
""".strip().splitlines()
KEYWORDS = "automation api testautomation testing qa openapi"
DESCRIPTION = "Test framework for auto-generating libraries from OpenAPI specification file"

setup(
    name=f"{PACKAGE}",
    version=__version__,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url=f"https://github.com/MarketSquare/{PACKAGE}",
    download_url=f"https://pypi.org/project/{PACKAGE}",
    author="Mateusz Nojek, Bartlomiej Hirsz",
    author_email="matnojek@gmail.com, bartek.hirsz@gmail.com",
    license="Apache License 2.0",
    platforms="any",
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=[PACKAGE],
    include_package_data=True,
    install_requires=[
        "black>=22.3",
        "robotframework>=4.1",
        "requests>=2.26",
        "urllib3>=1.26",
        "pyyaml>=6.0",
        "jinja2>=3.0",
        "prance>=0.21.8",
        "toml>=0.10.2",
        "openapi-spec-validator>=0.3",
        "jsonschema>=4.2.1",
    ],
    extras_requires={
        "dev": ["pytest", "black", "isort"],
    },
    entry_points={"console_scripts": [f"{PACKAGE}={PACKAGE}:run_roboswag"]},
)
