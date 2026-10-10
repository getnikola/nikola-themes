#!/bin/sh
set -e
cd site
nikola build
nikola deploy
