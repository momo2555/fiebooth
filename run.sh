#!/bin/bash

# Run Fiebooth 
cd /fiebooth/fiebooth
cd src
source ~/.bashrc
export "XAUTHORITY=$HOME/.Xauthority"
export "PYTHONPATH=$PYTHONPATH:$HOME/.pyenv/versions/fiebooth/lib/python3.9/site-packages"
export XDG_RUNTIME_DIR=/run/user/$(id -u)
DISPLAY=:0 XAUTHORITY=$XAUTHORITY  /home/fiebooth/.pyenv/versions/fiebooth/bin/python main.py &
cd ..

# Run Portail
cd portail
sudo python -m http.server 80 &
cd ..

pids=$(jobs -p)
kill_processes() {
  for pid in $pids; do
    kill $pid
  done
}
trap 'kill_processes' SIGINT

wait
