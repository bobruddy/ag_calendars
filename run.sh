#!/usr/bin/env bash

. .venv/bin/activate
python3 get_cal.py
. .env

rsync -av ./${AG_SAVE_DIR}/ ${AG_DEST_SERVER}:${AG_DEST_BASE_DIR}${AG_SAVE_DIR}/
