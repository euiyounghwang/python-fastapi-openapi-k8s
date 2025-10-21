

#!/bin/bash
set -e

# PYTHONDONTWRITEBYTECODE is an environment variable in Python that, when set to a non-empty string (commonly 1), 
# prevents Python from writing .pyc files to disk when importing source modules
export PYTHONDONTWRITEBYTECODE=1

JAVA_HOME='C:\Users\euiyoung.hwang\'
PATH=$PATH:$JAVA_HOME
export JAVA_HOME


SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTDIR

VENV=".venv"

# Python 3.11.7 with Window
if [ -d "$VENV/bin" ]; then
    source $VENV/bin/activate
else
    source $VENV/Scripts/activate
fi


# -- background
#  sudo netstat -nlp | grep :8002
# nohup $SCRIPTDIR/service-start.sh &> /dev/null &

# gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8888 --workers 4
# gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8888 --workers 4 --timemot 120
python -m uvicorn main:app --reload --host=0.0.0.0 --port=8888 --workers 1
# poetry run uvicorn main:app --reload --host=0.0.0.0 --port=8888 --workers 4
