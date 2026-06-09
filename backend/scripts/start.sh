#!/bin/sh
set -e

alembic upgrade head

fastapi run src/main.py --workers 4
