#!/bin/bash

rm -rf .eggs
rm -rf AUTHORS
rm -rf breadbot.egg-info
rm -rf build
rm -rf ChangeLog
find -name "__pycache__" | xargs rm -rf
echo "Done"
