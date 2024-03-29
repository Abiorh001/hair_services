#!/bin/bash

# bash script to install docker and docker-compose and pip for Python 3 on Ubuntu server

# Update package lists
sudo apt-get update -y

# Install Docker
sudo apt-get install -y docker

# Install Docker Compose
sudo apt-get install -y docker-compose

# Start Docker
sudo service docker start

# Install pip for Python 3
sudo apt-get install -y python3-pip
