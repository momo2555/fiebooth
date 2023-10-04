#!/bin/bash
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd
sudo cp files/dhcpcd-wifi.conf /etc/dhcpcd.conf
sudo service dhcpcd restart
#sudo ifdown wlan0
#sleep 1
#sudo ifup wlan0