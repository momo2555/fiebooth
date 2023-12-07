#!/bin/bash
sudo rfkill block wifi
sleep 1

SSID=$(cat /fiebooth/config/.ssid)
sudo cp files/dhcpcd-ap.conf /etc/dhcpcd.conf
#sudo cp files/hostapd.conf /etc/hostapd/hostapd.conf
#sudo sed -i -e "s/_ssid_/$SSID/g" /etc/hostapd/hostapd.conf
sudo service dhcpcd restart
sleep 1
sudo systemctl start dnsmasq
#sudo systemctl start hostapd
