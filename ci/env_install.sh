#!/usr/bin/env bash

echo "Creating a Python $PYTHON_VERSION environment"
conda create -n logofinder python=$PYTHON_VERSION flake8 scrapy nose || exit 1
