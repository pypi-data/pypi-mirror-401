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
from nanocore.models.inventory import NanocoreItem as Item
from nanocore.models.inventory import NanocoreInventory as Inventory
from nanocore.models.inventory import NanocoreInventoryRequest as Request
from nanocore.models.inventory import NanocoreInventoryResponse as Response

# ---------------------------------------------------------
# Dynamic Loading Interface / EP Exposure
# ---------------------------------------------------------
TAG = "Inventory"
DESCRIPTION = "Inventory CLI API"
API_ORDER = 10

# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------

from agptools.logs import logger

log = logger(__name__)


# ---------------------------------------------------------
# Inventory CLI router
# ---------------------------------------------------------
@main.group(context_settings=CONTEXT_SETTINGS)
@click.pass_obj
def inventory(env):
    """subcommands for managing inventory for nanocore"""
    # banner("User", env.__dict__)


submodule = inventory


@submodule.command()
@click.option("--path", default=None)
@click.pass_obj
def create(env, path):
    """Create a new inventory item for nanocore"""
    # force config loading
    config.callback()

    # TODO: implement


@submodule.command()
@click.pass_obj
def read(env):
    """Find and list existing inventory items for nanocore"""
    # force config loading
    config.callback()

    # TODO: implement


@submodule.command()
@click.pass_obj
def update(env):
    """Update and existing inventory item for nanocore"""
    # force config loading
    config.callback()

    # TODO: implement


@submodule.command()
@click.pass_obj
def delete(env):
    """Delete an existing inventory item for nanocore"""
    # force config loading
    config.callback()

    # TODO: implement
