#!/bin/bash

pip install -r requirements.txt

sudo apt-get update

sudo apt-get install git -y

sudo apt install libopengl0 -y

python3.9 AFiT.py
