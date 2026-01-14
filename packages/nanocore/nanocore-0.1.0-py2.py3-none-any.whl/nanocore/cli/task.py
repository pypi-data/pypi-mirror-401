# import re
# import os
# import yaml

import click

# from nanocore.helpers import *
from nanocore.cli.main import main, CONTEXT_SETTINGS
from nanocore.cli.config import config

from nanocore.definitions import DEFAULT_LANGUAGE, UID_TYPE

# TODO: include any logic from module core
# Examples
# from nanocore.models import *
# from nanocore.logic import Tagger
# from syncmodels.storage import Storage

# Import local inventory models
from nanocore.models.task import NanocoreTask as Item
from nanocore.models.task import NanocoreTaskRequest as Request
from nanocore.models.task import NanocoreTaskResponse as Response

# ---------------------------------------------------------
# Dynamic Loading Interface / EP Exposure
# ---------------------------------------------------------
TAG = "Tasks"
DESCRIPTION = "Tasks CLI API"
API_ORDER = 10

# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------

from agptools.logs import logger

log = logger(__name__)


# ---------------------------------------------------------
# Task CLI port implementation
# ---------------------------------------------------------
@main.group(context_settings=CONTEXT_SETTINGS)
@click.pass_obj
def task(env):
    """subcommands for managing tasks for nanocore"""
    # banner("User", env.__dict__)


submodule = task


@submodule.command()
@click.option("--path", default=None)
@click.pass_obj
def create(env, path):
    """Create a new task for nanocore"""
    # force config loading
    config.callback()

    # TODO: implement


@submodule.command()
@click.pass_obj
def read(env):
    """Find and list existing tasks for nanocore"""
    # force config loading
    config.callback()

    # TODO: implement


@submodule.command()
@click.pass_obj
def update(env):
    """Update and existing task for nanocore"""
    # force config loading
    config.callback()

    # TODO: implement


@submodule.command()
@click.pass_obj
def delete(env):
    """Delete an existing task for nanocore"""
    # force config loading
    config.callback()

    # TODO: implement
