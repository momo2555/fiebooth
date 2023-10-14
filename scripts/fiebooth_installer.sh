#!/bin/bash

sudo mkdir /fiebooth
sudo chown "$USER" /fiebooth
sudo chmod 755 /fiebooth

ssh-keygen -t rsa -b 4096 -C "mohamed.alglawi@gmail.com"
cat .ssh/id_rsa.pub

cd /fiebooth
git clone git@github.com:momo2555/fiebooth.git