"""
This script is executed as a cron job every minute. It checks if the remote
`deps.zip` file has been updated. If it has, it touches the  uwsgi_trigger file
that cause uWSGI to reload the application.
"""

import datetime
import os
import shutil

from django.core.files.storage import storages

DEPS_DIR = "/openedx/live-dependencies/deps"
DEPS_KEY = "deps.zip"
TRIGGER_FILE = "/openedx/live-dependencies/uwsgi_trigger"
TIMESTAMP_FILE = "/openedx/live-dependencies/last_update_timestamp"


def main():
    # TODO Use a separate storage for live dependencies
    storage = storages["default"]

    if storage.exists(DEPS_KEY):
        remote_ts = storage.get_modified_time(DEPS_KEY)
        with open(TIMESTAMP_FILE, "r") as f:
            local_ts_str = f.read().strip()
            if local_ts_str:
                local_ts = datetime.datetime.fromisoformat(local_ts_str)

        if local_ts < remote_ts:
            with open(TRIGGER_FILE, "a"):
                os.utime(TRIGGER_FILE, None)
    else:
        # If the deps.zip file has been deleted from the storage backend, remove the local deps
        if os.path.exists(DEPS_DIR):
            shutil.rmtree(DEPS_DIR)
            with open(TRIGGER_FILE, "a"):
                os.utime(TRIGGER_FILE, None)


if __name__ == "__main__":
    main()
