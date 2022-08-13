# pylint: disable=missing-function-docstring, unused-argument
import pathlib
import subprocess

from invoke import task

ROOT = pathlib.Path(__file__).parent.resolve().as_posix()


@task
def lint(context):
    subprocess.run(f"mypy {ROOT}", shell=True, check=False)
    subprocess.run(f"pylint {ROOT}/roboswag", shell=True, check=False)


@task
def format_code(context):
    subprocess.run(f"black {ROOT}", shell=True, check=False)
    subprocess.run(f"isort {ROOT}", shell=True, check=False)


@task(format_code)
def build(context):
    subprocess.run("poetry build", shell=True, check=False)


@task(post=[build])
def bump_version(context, rule):
    subprocess.run(f"poetry version {rule}", shell=True, check=False)
    subprocess.run("poetry install", shell=True, check=False)
