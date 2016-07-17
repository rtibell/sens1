#!/bin/bash
rm *.pyc
git status
git add Accelerometer.py Runner.py Display.py DBController.py push.sh FileController.py BinaryFileController.py
git add REST.py html/chart.js html/graph.html
git commit -m 'upd'
git push origin master
