#!/bin/bash
#sudo apt install ./drivers/drivers/ql800pdrv-2.1.4-0.armhf.deb

#curl https://pyenv.run | bash
#echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
#echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
#echo 'eval "$(pyenv init -)"' >> ~/.bashrc
#source ~/.bashrc
#pyenv install 3.9.2
pushd ..
# python env install
python -m pip install requirements.txt

# install camera
wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
chmod +x install_pivariety_pkgs.sh
./install_pivariety_pkgs.sh -p libcamera_dev
./install_pivariety_pkgs.sh -p libcamera_apps
./install_pivariety_pkgs.sh -p 64mp_pi_hawk_eye_kernel_driver

# configure printer
sudo usermod -a -G lpadmin fiebooth
sudo usermod -a -G lp fiebooth

# install infra
sudo apt install -y hostapd dnsmasq
sudp cp scrpts/files/hostapd.conf /etc/hostapd/hostapd.conf
sudo echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' >> /etc/default/hostapd #fin du fichier
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo cp scripts/files/dnsmasq.conf /etc/dnsmasq.conf
sudo echo "192.168.42.10 portail.fiebooth" >> sudo nano /etc/hosts # fin du fichier
sudo cp scripts/files/dhcpcd-ap.conf /etc/dhcpcd.conf

# auto run on fiebooh :
# ...

# reboot raspberry pi
sudo reboot
popd 
# dtoverlay=vc4-kms-v3d,cma-512 > /boot/config.txt [pi4]

