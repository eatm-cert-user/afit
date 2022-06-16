#!/bin/bash

sudo apt update

sudo add-apt-repository -y ppa:openjdk-r/ppa
sudo apt-get update

wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt-get update

sudo apt install neo4j

sudo systemctl enable neo4j.service