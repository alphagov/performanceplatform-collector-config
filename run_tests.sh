#!/bin/bash -e

set -o pipefail

python -m doctest tools/cronjobs.py -v
