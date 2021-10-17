import pathlib
from setuptools import setup


PACKAGE = "rfopenapi"
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
KEYWORDS = "robotframework automation testautomation testing qa API OpenAPI"
DESCRIPTION = "Test framework for API with usage of Robot Framework"

setup(
    name=f"robotframework-{PACKAGE}",
    version=__version__,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url=f"https://github.com/bhirsz/robotframework-{PACKAGE}",
    download_url=f"https://pypi.org/project/robotframework-{PACKAGE}",
    author="Bartlomiej Hirsz, Mateusz Nojek",
    author_email="bartek.hirsz@gmail.com, matnojek@gmail.com",
    license="Apache License 2.0",
    platforms="any",
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=[PACKAGE],
    include_package_data=True,
    install_requires=["robotframework>=3.2.2", "toml>=0.10.2"],
    extras_requires={
        "dev": ["pytest", "black"],
        # "doc": ["sphinx", "sphinx_rtd_theme"],
    },
    entry_points={"console_scripts": [f"{PACKAGE}={PACKAGE}.generate:generate"]},
)
