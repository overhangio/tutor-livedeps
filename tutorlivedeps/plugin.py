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
        ("LIVEDEPS", []),
    ]
)

########################################
# INITIALIZATION TASKS
########################################


MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    ("minio", ("livedeps", "tasks", "minio", "init.sh")),
]

for service, template_path in MY_INIT_TASKS:
    full_path: str = str(
        importlib_resources.files("tutorlivedeps")
        / os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


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
def livedeps(context: Context) -> t.Iterable[tuple[str, str]]:
    """
    Calls the build function in livedeps with the list of packages
    specified in the LIVEDEPS configuration variable.
    """

    config = tutor_config.load(context.root)
    all_packages = " ".join(
        package for package in t.cast(list[str], config["LIVEDEPS"])
    )
    script = f"livedeps build {all_packages}"

    yield ("lms", script)


hooks.Filters.CLI_DO_COMMANDS.add_item(livedeps)
