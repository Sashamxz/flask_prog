#!/bin/bash

source env/bin/activate

# while true; do
#     flask db upgrade
#     if [[ "$?" == "0" ]]; then
#         break
#     fi
#     echo Upgrade command failed, retrying in 5 secs...
#     sleep 5
# done

flask db migrate
exec gunicorn -b :7777  --access-logfile - --error-logfile - flask_proj:app