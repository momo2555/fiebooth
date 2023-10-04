#!/bin/bash
sudo cp files/dhcpcd-ap.conf /etc/dhcpcd.conf
sudo service dhcpcd restart
sleep 1
sudo systemctl start dnsmasq
sudo systemctl start hostapd

