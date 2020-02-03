#!/usr/bin/env bash
# This script is meant for developer use only
# Does not support its path being moved
# Depends on Python environment being set up and active

THIS_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYTHONPATH="${THIS_SCRIPT_DIR}"
FLASK_APP="${THIS_SCRIPT_DIR}/api/index.py"
export PYTHONPATH FLASK_APP
flask run
