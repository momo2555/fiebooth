#!/bin/bash

# Run Fiebooth 
cd /fiebooth/fiebooth
cd src
source ~/.bashrc
export "XAUTHORITY=$HOME/.Xauthority"
export "PYTHONPATH=$PYTHONPATH:/fiebooth/fiebooth/env/site-packages"
export XDG_RUNTIME_DIR=/run/user/$(id -u)
DISPLAY=:0 XAUTHORITY=$XAUTHORITY  /fiebooth/fiebooth/env/python main.py &
cd ..

# Run Portail
cd portail
sudo python -m http.server 80 &
cd ..

pids=$(jobs -p)
echo "jobs = $pids"
kill_processes() {
  echo "kill every body !! :)"
  kill $!
  for pid in $pids; do
    kill $pid
  done
}
trap 'kill_processes' SIGINT

wait
