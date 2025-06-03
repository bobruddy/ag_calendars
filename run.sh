#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd ${SCRIPT_DIR}

. .venv/bin/activate
python3 get_cal.py
. .env
cp index.html ${AG_SAVE_DIR}

rsync -av ./${AG_SAVE_DIR}/ ${AG_DEST_SERVER}:${AG_DEST_BASE_DIR}${AG_SAVE_DIR}/

cd -
