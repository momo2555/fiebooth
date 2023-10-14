#!/bin/bash
#sudo apt install ./drivers/drivers/ql800pdrv-2.1.4-0.armhf.deb

sudo apt-get update; 
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
 libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils \
 tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
git clone https://github.com/yyuu/pyenv.git "$HOME/.pyenv"

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
#curl https://pyenv.run | bash
#echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
#echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
#echo 'eval "$(pyenv init -)"' >> ~/.bashrc
#source ~/.bashrc
#pyenv install 3.9.2
#pushd ..
# python env install
#echo "Update python environment ..."
#python -m pip install requirements.txt

#install fiebooth portail
#echo "Install Fiebooth Portail ..."
#bash scripts/install_portail.sh

# install camera
#echo "Install camera drivers ..."
#wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
#chmod +x install_pivariety_pkgs.sh
#./install_pivariety_pkgs.sh -p libcamera_dev
#./install_pivariety_pkgs.sh -p libcamera_apps
#./install_pivariety_pkgs.sh -p 64mp_pi_hawk_eye_kernel_driver
# dtoverlay=vc4-kms-v3d,cma-512 > /boot/config.txt [pi4]

# configure printer
#echo "Configure printer ..."
#sudo usermod -a -G lpadmin fiebooth
#sudo usermod -a -G lp fiebooth

# install infra
#echo "Install infra, setup DNS and wifi Accsess Point ..."
#sudo apt install -y hostapd dnsmasq
#sudo cp scripts/files/hostapd.conf /etc/hostapd/hostapd.conf
#sudo cp scripts/files/hostapd /etc/default/hostapd #fin du fichier
#sudo systemctl unmask hostapd
#sudo systemctl enable hostapd
#sudo cp scripts/files/dnsmasq.conf /etc/dnsmasq.conf
#sudo cp scripts/files/hosts /etc/hosts # fin du fichier
#sudo cp scripts/files/dhcpcd-ap.conf /etc/dhcpcd.conf

# auto run on fiebooh :
#echo "Setup systemd service for Fiebooth ..."
#sudo cp scripts/files/fiebooth.service /etc/systemd/system/fiebooth.service
#sudo systemctl daemon-reload
#sudo systemctl enable fiebooth.service

# reboot raspberry pi
echo "Reboot Fiebooth ..."
#sudo reboot
#popd 

