#!/bin/bash

# Run Fiebooth 
pushd src
python main.py &
popd

# Run Portail
pushd portail
python -m http.server 80 &
popd

