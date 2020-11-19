import os
import shutil
from glob import glob
from invoke import task

CLEAN_PATTERNS = [
    "dist",
    ".pytest_cache",
    "**/__pycache__",
    "**/*.pyc",
    "**/*.egg-info",
]


@task
def clean(ctx):
    """Remove all generated files."""
    for pattern in CLEAN_PATTERNS:
        for path in glob(pattern):
            shutil.rmtree(path, ignore_errors=True)


@task
def install(ctx):
    """Install development environment."""
    ctx.run("poetry install")


@task(install)
def lint(ctx):
    """Run autoformat and static analysis."""
    print("Running black")
    ctx.run("poetry run black skeltal")

    print("Running flake8")
    ctx.run("poetry run flake8 --config .flake8 skeltal")

    print("Running pylint")
    ctx.run("poetry run pylint --rcfile .pylintrc skeltal")

    print("Running mypy")
    ctx.run("poetry run mypy ")


@task(install)
def test(ctx):
    """Run unittests."""
    ctx.run("poetry run pytest -v tests/")


@task(install)
def run(ctx):
    """Start skeltal."""
    ctx.run("poetry run skel")


@task(lint, test)
def build(ctx):
    """Build distributable package."""
    ctx.run("poetry build -v")


@task(clean, build)
def publish(ctx):
    """Publish package to PyPI."""
    ctx.run("poetry publish -v")
