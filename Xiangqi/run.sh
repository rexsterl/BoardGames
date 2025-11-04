#!/bin/bash
# Launch script for Xiangqi game
# Sets PYTHONPATH to project root

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH="$SCRIPT_DIR"

python3 main.py
