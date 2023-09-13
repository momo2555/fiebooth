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
copy the content in SSH key creation in github : https://github.com/settings/keys \
- Click on create new SSH key
- Add a key name
- And copy the the public key
- Save the key

## Clone the project
``` 
git clone git@github.com:momo2555/fiebooth.git
```

## Install python3:
```
sudo apt install -y python3 build-essential libssl-dev libffi-dev python3-dev
```
## Setup an environment:
```
sudo appt install python-venv
cd fiebooth
pyhon -m venv fiebooth
source fiebooth/bin/activate
pip install -r requirments.txt
```

## notice hawkeye
https://gist.github.com/geerlingguy/de62619a906803808edddaf8bb9cdce8

- Download the pivariety driver install script and make it executable
```
wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
chmod +x install_pivariety_pkgs.sh
```

- Install libcamera dev and apps
```
./install_pivariety_pkgs.sh -p libcamera_dev
./install_pivariety_pkgs.sh -p libcamera_apps
```

- Install the Hawk-Eye kernel driver
```
./install_pivariety_pkgs.sh -p 64mp_pi_hawk_eye_kernel_driver
```

- Edit /boot/config.txt, and under [pi4] section, add this line:
```
dtoverlay=vc4-kms-v3d,cma-512
```

- After a reboot, Tast the camera by taking a picture with autofocus at 16 megapixels:
```
libcamera-still -t 5000 --viewfinder-width 2312 --viewfinder-height 1736 --width 4624 --height 3472 -o 16mp-autofocus-test.jpg
```

## code photobooth var/html /... (not necessary, we have our own API !! :D)
https://trevilly.com/borne-photos-autonome-automatique-et-avec-galerie-web-integree-raspberry-pi/

## install printer driver (not working for me)
### Disable sleep time
### Installation
### Test
```
cd drivers
sudo apt install ./driver_name.deb
```

## get printer name
```
lpstat -p
```

## Create a .env file with parameters
```
ADMIN_PASSWORD=adminpassword
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## TODO
- Add an indtall.sh script
- Add gen_config.sh script
- Add brother_ql library in driver folder (and fork the project)
- Create web interface
