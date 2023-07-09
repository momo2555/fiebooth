# Fiebooth

## Connect the Raspberry pi
Connect the Raspberry pi to your network
Or follow this link : https://howchoo.com/g/ndy1zte2yjn/how-to-set-up-wifi-on-your-raspberry-pi-without-ethernet

## Enable SSH on your rpi
Set up the ssh in the config menu of the RPi
Or follow this link : https://howchoo.com/g/ote0ywmzywj/how-to-enable-ssh-on-raspbian-without-a-screen

## Create a RSA key
```
ssh-keygen -t rsa -b 4096 -C "mohamed.alglawi@gmail.com"
cat .ssh/id_rsa.pub
```
copy the content in SSH key creation in github

## Clone the project
``` 
git clone
```

## Install python3:
```
sudo apt install -y python3 build-essential libssl-dev libffi-dev python3-dev
```
## Setup an environment
```
sudo appt install python-venv
cd fiebooth
pyhon -m venv fiebooth
source fiebooth/bin/activate
pip install -r requirments.txt
```

## notice hawkeye
https://gist.github.com/geerlingguy/de62619a906803808edddaf8bb9cdce8

## code photobooth var/html /... 
https://trevilly.com/borne-photos-autonome-automatique-et-avec-galerie-web-integree-raspberry-pi/