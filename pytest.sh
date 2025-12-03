set -e

# PYTHONDONTWRITEBYTECODE is an environment variable in Python that, when set to a non-empty string (commonly 1), 
# prevents Python from writing .pyc files to disk when importing source modules
export PYTHONDONTWRITEBYTECODE=1


SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTDIR

VENV=".venv"

# Python 3.11.7 with Window
if [ -d "$VENV/bin" ]; then
    source $VENV/bin/activate
else
    source $VENV/Scripts/activate
fi


# py.test -v tests
pytest -v tests
# py.test -v ./tests --cov-report term-missing --cov
# poetry run py.test -sv ./tests --disable-warnings --cov-report term-missing --cov