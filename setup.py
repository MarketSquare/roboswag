import pathlib

from setuptools import setup

PACKAGE = "openapi"
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
with open(HERE / PACKAGE / "version.py") as f:
    __version__ = f.read().split("=")[1].strip().strip('"')
CLASSIFIERS = """
Development Status :: 2 - Pre-Alpha
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Framework :: Robot Framework
Framework :: Robot Framework :: Tool
Topic :: Software Development :: Testing
Topic :: Software Development :: Quality Assurance
Topic :: Utilities
Intended Audience :: Developers
""".strip().splitlines()
KEYWORDS = "robotframework automation testautomation testing qa"
DESCRIPTION = "Test framework for API with usage of Robot Framework"

setup(
    name=f"robotframework-{PACKAGE}",
    version=__version__,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url=f"https://github.com/bhirsz/robotframework-{PACKAGE}",
    download_url=f"https://pypi.org/project/robotframework-{PACKAGE}",
    author="Mateusz Nojek, Bartlomiej Hirsz",
    author_email="matnojek@gmail.com, bartek.hirsz@gmail.com",
    license="Apache License 2.0",
    platforms="any",
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=[PACKAGE],
    include_package_data=True,
    install_requires=[
        "robotframework>=4.1",
        "requests>=2.26",
        "urllib3>=1.26",
        "pyyaml>=6.0",
        "jinja2>=3.0",
        "prance>=0.21.8",
        "toml>=0.10.2",
        "openapi-spec-validator>=0.3",
    ],
    extras_requires={
        "dev": ["pytest", "black", "isort"],
    },
    entry_points={"console_scripts": [f"{PACKAGE}={PACKAGE}:run_openapi"]},
)
