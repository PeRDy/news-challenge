#!/usr/bin/env bash

# Install docker
echo "Install Docker"
sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
lsb_release -a | grep Codename | awk 'match($0, /Codename:\s+(\w+)/, a) { printf "deb https://apt.dockerproject.org/repo ubuntu-%s main\n", a[1] }' | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update && sudo apt-get install -y docker-engine

# Install docker-compose
echo "Install docker-compose"
curl -L https://github.com/docker/compose/releases/download/1.7.1/docker-compose-`uname -s`-`uname -m` | sudo tee /usr/local/bin/docker-compose > /dev/null && \
sudo chmod +x /usr/local/bin/docker-compose

# Install docker-machine
echo "Install docker-machine"
curl -L https://github.com/docker/machine/releases/download/v0.7.0/docker-machine-`uname -s`-`uname -m` | sudo tee /usr/local/bin/docker-machine > /dev/null && \
sudo chmod +x /usr/local/bin/docker-machine

# Install Virtualbox
sudo apt-get install virtualbox

# Create docker-machine environment
echo "Create docker-machine environment"
docker-machine create --driver virtualbox default
docker-machine start default
eval `docker-machine env default`

# Build containers
echo "Build containers"
docker-compose build

# Run build configuration
echo "Run app build configuration"
docker-compose run news build

# Load data
echo "Load app data files"
docker-compose run news load audience audience.json
docker-compose run news load segments segments.json
