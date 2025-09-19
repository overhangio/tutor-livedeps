import datetime
import time

from django.core.files.storage import storages

DEPS_KEY = "deps.zip"
TRIGGER_FILE = "/openedx/live-dependencies/uwsgi_trigger"

# TODO Use a separate storage for live dependencies
storage = storages["default"]

while True:
    if storage.exists(DEPS_KEY):
        remote_ts = storage.get_modified_time(DEPS_KEY)
        local_ts = None
        with open(TRIGGER_FILE, "r") as f:
            local_ts_str = f.read().strip()
            if local_ts_str:
                local_ts = datetime.datetime.fromisoformat(local_ts_str)

        if local_ts is None or local_ts < remote_ts:
            now = datetime.datetime.now(tz=datetime.timezone.utc)
            with open(TRIGGER_FILE, "w") as f:
                # Writing to the TRIGGER_FILE will cause uWSGI to reload the app
                f.write(now.isoformat())
    time.sleep(10)
