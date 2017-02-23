#!/usr/bin/env bash

echo "Testing installation in Python $PYTHON_VERSION environment"
export PATH="$HOME/miniconda3/envs/logofinder/bin:$PATH"

flake8 --filename=*.py
python testspider.py
