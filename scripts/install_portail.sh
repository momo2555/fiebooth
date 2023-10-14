#!/bin/bash

wget -O portail.zip https://github.com/momo2555/fiebooth_portail/releases/download/FIEBOOTH_PORTAIL_0.2/fiebooth_portail_0.2.zip
unzip portail.zip
if [ -d "portail" ]; then
    rm -rf portail
fi
mv web portail
rm -f portail.zip
