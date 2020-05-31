#!/usr/bin/env bash

python3 LogCollectDaemon.py &

python3 LogCycle.py &

python3 manage.py runserver
