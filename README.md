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
```
cd drivers
sudo apt install ./driver_name.deb
```

### Disable sleep time
See the link : 
### Installation
add lp and lpadmin to the user group (so that python can right on the printer)
```
sudo usermod -a -G lpadmin fiebooth
sudo usermod -a -G lp fiebooth
sudo reboot
```
### Test

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
## DNS and DHCP configuration
https://raspberrytips.fr/serveur-dns-local-raspberry-pi/ \
https://raspberrytips.com/dhcp-server-on-raspberry-pi/

## Install docker (NO NEED OF DOCKER, NOT WORKING WELL)
```
cd ~
sudo apt-get update && sudo apt-get upgrade
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker [user_name]  <= "fiebooth"
```

## Install dsnmasq
```
sudo apt install hostapd dnsmasq
```
### Config hostapd
```
sudo nano /etc/hostapd/hostapd.conf
```
Add this config
```
interface=wlan0
driver=nl80211
ssid=fiebooth
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=fiebooth
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

```
sudo nano /etc/default/hostapd
```
Add this lin :
```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
```

### Config DNS server
```
sudo nano /etc/dnsmasq.conf
```
Add this config
```
interface=wlan0
bind-dynamic
domain-needed
bogus-priv
expand-hosts
dhcp-range=192.168.42.100,192.168.42.200,255.255.255.0,12h
domain=fiebooth
```
Add the new domain
```
sudo nano /etc/hosts
```

### Configure the DHCP
```
sudo nano /etc/dhcpcd.conf
```
Add those line at the end of the file
```
nohook wpa_supplicant
interface wlan0
static ip_address=192.168.42.10/24
static routers=192.168.42.1
```
Now reboot
## TODO
- Add an indtall.sh script
- Add gen_config.sh script
- Add brother_ql library in driver folder (and fork the project)
- Create web interface (work in progress)
- pagination system (not prio)
- dockerise all

