#!/bin/bash -x
PWD=`pwd`
python3 -m venv .venv
activate () {
    . $PWD/.venv/bin/activate
}

activate

python3 -m pip install -r requirements.txt