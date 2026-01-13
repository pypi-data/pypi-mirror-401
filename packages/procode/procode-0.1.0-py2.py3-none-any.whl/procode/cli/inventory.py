# import re
# import os
# import yaml

import click

# from procode.helpers import *
from procode.cli.main import main, CONTEXT_SETTINGS
from procode.cli.config import config


from procode.definitions import DEFAULT_LANGUAGE, UID_TYPE

# TODO: include any logic from module core
# Examples
# from procode.models import *
# from procode.logic import Tagger
# from syncmodels.storage import Storage

# Import local inventory models
from procode.models.inventory import ProcodeItem as Item
from procode.models.inventory import ProcodeInventory as Inventory
from procode.models.inventory import ProcodeInventoryRequest as Request
from procode.models.inventory import ProcodeInventoryResponse as Response

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
    """subcommands for managing inventory for procode"""
    # banner("User", env.__dict__)


submodule = inventory


@submodule.command()
@click.option("--path", default=None)
@click.pass_obj
def create(env, path):
    """Create a new inventory item for procode"""
    # force config loading
    config.callback()

    # TODO: implement


@submodule.command()
@click.pass_obj
def read(env):
    """Find and list existing inventory items for procode"""
    # force config loading
    config.callback()

    # TODO: implement


@submodule.command()
@click.pass_obj
def update(env):
    """Update and existing inventory item for procode"""
    # force config loading
    config.callback()

    # TODO: implement


@submodule.command()
@click.pass_obj
def delete(env):
    """Delete an existing inventory item for procode"""
    # force config loading
    config.callback()

    # TODO: implement
