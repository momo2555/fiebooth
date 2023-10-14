#!/bin/bash

# Run Fiebooth 
cd src
DISPLAY=:0 python main.py &
cd ..

# Run Portail
cd portail
sudo python -m http.server 80 &
cd ..

wait
