import os
import typing as t
from glob import glob

import click
import importlib_resources
from tutor import config as tutor_config
from tutor import hooks
from tutor.commands.context import Context

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        ("LIVEDEPS_VERSION", __version__),
        ("LIVE_DEPENDENCIES", []),
    ]
)


########################################
# TEMPLATE RENDERING
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        str(importlib_resources.files("tutorlivedeps") / "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("livedeps/build", "build/openedx/settings"),
    ],
)


########################################
# PATCH LOADING
########################################


for path in glob(str(importlib_resources.files("tutorlivedeps") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################


@click.command(
    help="Build all live dependencies, zip them and upload to storage backend"
)
@click.pass_obj
def build_live_dependencies(context: Context) -> t.Iterable[tuple[str, str]]:
    """
    Build the live dependencies and upload using Django's storage API.
    You need to update the `LIVE_DEPENDENCIES` variable in the config file to add/remove packages.
    """
    config = tutor_config.load(context.root)
    all_packages = " ".join(
        package for package in t.cast(list[str], config["LIVE_DEPENDENCIES"])
    )
    if not all_packages:
        # Delete the deps.zip file if the LIVE_DEPENDENCIES list is empty
        script = """
        python3 -c '
from django.core.files.storage import storages
DEPS_KEY = "deps.zip"
storages["default"].delete(DEPS_KEY)
'
        """
    else:
        script = f"""
        pip install \
        --prefix=/openedx/live-dependencies/deps \
        {all_packages} \
        && python3 -c '
import os, shutil, tempfile
from django.core.files.storage import storages
from django.core.files.base import File

DEPS_DIR = "/openedx/live-dependencies/deps"
DEPS_KEY = "deps.zip"

with tempfile.TemporaryDirectory(prefix="tutor-livedeps-") as zip_dir:
    base = os.path.join(zip_dir, DEPS_KEY)
    archive_path = shutil.make_archive(base[:-4], format="zip", root_dir=DEPS_DIR)

    with open(archive_path, "rb") as f:
        # TODO Use a separate storage for live dependencies
        storages["default"].save(DEPS_KEY, File(f))
'
        """

    yield ("lms", script)


hooks.Filters.CLI_DO_COMMANDS.add_item(build_live_dependencies)
