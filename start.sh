#!/bin/bash
#

source env/bin/activate


flask db upgrade
  
exec gunicorn --bind 0.0.0.0:5000  --access-logfile - --error-logfile - flask_proj:app