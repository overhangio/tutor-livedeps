
<a id='changelog-21.0.0'></a>
## v21.0.0 (2026-01-20)

- [Feature] Add python dependencies at runtime without rebuilding image. (by @mlabeeb03)

- [Improvement] Remove deps.zip file after extracting the packages. (by @mlabeeb03)

- [Improvement] Use uwsgi cron instead of a daemon to run monitor_livedeps.py script. (by @mlabeeb03)
- [Improvement] Use the last_update_timestamp file to check for the local timestamp of dependencies. (by @mlabeeb03)

- [Bugfix] Fix job runner error when LIVE_DEPENDENCIES config is empty. (by @mlabeeb03)

- [Bugfix] Delete the local deps directory if deps.zip is deleted from storage. (by @mlabeeb03)

- [Improvement] Merge all scripts related to livedeps into one file, create init job, update docs and lots of refactoring. (by @mlabeeb03)

- [Improvement] Remove init job. (by @mlabeeb03)

- 💥[Feature] Upgrade to Ulmo. (by @mlabeeb03)
