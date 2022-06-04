#!/bin/bash

pip3 install --user -r requirements.txt
python3 setup.py install
cp -r files/ ~/.breadbot/
git clone https://github.com/ideamark/ideamark.github.io ~/.breadbot/data
sed -in-place -e 's%~%'${HOME}'%g' ~/.breadbot/etc/bread.cfg