#!/usr/bin/env bash

echo "Creating a Python $PYTHON_VERSION environment"
conda create -n logofinder python=$PYTHON_VERSION flake8 scrapy nose Pillow || exit 1

export PATH="$HOME/miniconda3/envs/logofinder/bin:$PATH"
pip install tensorflow
