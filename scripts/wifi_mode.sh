#!/bin/bash
SSID="$1"
PSK="$2"
# stop dns server and AP
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd
# reconfigure wifi
cp files/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
sed ...
# restart the dhcp
sudo cp files/dhcpcd-wifi.conf /etc/dhcpcd.conf
sudo service dhcpcd restart
