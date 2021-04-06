#!/usr/bin/env bash

python3 add_barcode.py

git add .
git commit -m "Updated data.csv"
git push
