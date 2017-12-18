#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M%S")

raspistill -vf -o /home/pi/my_magic_mirror/static/selfies/$DATE.jpg
