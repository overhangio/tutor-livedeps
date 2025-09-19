"""
This script is executed every time the uwsgi server starts/restarts.
It downloads the live dependencies zip file and extracts it to a specified location.
It also updates the last_update_timestamp file that is used by the monitor_livedeps.py script.
"""

import datetime
import os
import shutil
import zipfile

from django.core.files.storage import storages

DEPS_DIR = "/openedx/live-dependencies/deps"
DEPS_KEY = "deps.zip"
DEPS_ZIP_PATH = DEPS_DIR[:-4] + DEPS_KEY
TIMESTAMP_FILE = "/openedx/live-dependencies/last_update_timestamp"


def main():
    # TODO Use a separate storage for live dependencies
    storage = storages["default"]

    if storage.exists(DEPS_KEY):
        if os.path.exists(DEPS_DIR):
            shutil.rmtree(DEPS_DIR)
        os.makedirs(DEPS_DIR, exist_ok=True)

        with (
            storage.open(DEPS_KEY, "rb") as remote_f,
            open(DEPS_ZIP_PATH, "wb") as local_f,
        ):
            shutil.copyfileobj(remote_f, local_f)

        with zipfile.ZipFile(DEPS_ZIP_PATH, "r") as zip_ref:
            zip_ref.extractall(DEPS_DIR)

        os.remove(DEPS_ZIP_PATH)

    # Store the timestamp of the latest update. If the remote deps.zip file is updated after
    # this timestamp, the monitor_livedeps.py script will trigger a reload.
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    with open(TIMESTAMP_FILE, "w") as f:
        f.write(now.isoformat())


if __name__ == "__main__":
    main()
