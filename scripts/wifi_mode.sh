#!/bin/bash
if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_file> <replacement>"
    exit 1
fi

# define ssid and pka
SSID=$1
PSK=$2

# stop dns server and AP
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd

# reconfigure wifi
cp files/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
sudo sed "/{ssid}/$SSID/g" /etc/wpa_supplicant/wpa_supplicant.conf
sudo sed "/{psk}/$psk/g" /etc/wpa_supplicant/wpa_supplicant.conf

# restart the dhcp with wifi configuration
sudo cp files/dhcpcd-wifi.conf /etc/dhcpcd.conf
sudo service dhcpcd restart
