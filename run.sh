#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd ${SCRIPT_DIR}
git pull

. .venv/bin/activate
python3 get_cal.py
. .env
cp index.html ${AG_SAVE_DIR}

oldest_file=$(ls -1t ${AG_SAVE_DIR}/*.ics | tail -n 1) 
formatted_date=$(date -r "${oldest_file}" +"%Y-%m-%d %H:%M")
sed "s/update_date/${formatted_date}/" index.html > ${AG_SAVE_DIR}/index.html

rsync -av ./${AG_SAVE_DIR}/ ${AG_DEST_SERVER}:${AG_DEST_BASE_DIR}${AG_SAVE_DIR}/

cd -
