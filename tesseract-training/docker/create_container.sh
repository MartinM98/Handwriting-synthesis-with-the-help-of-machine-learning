#!/bin/bash

docker pull ubuntu # pull the latest Ubuntu image

docker run --name ubuntu-container -it ubuntu:latest bash # create new container with the name ubuntu-container. Additionally, bash option is added to the docker command so that the container could be accessed

docker cp $1 ubuntu-container:/root/tesstrain # copy file/directory for which the path was given by the argument to the home directory in the container image

docker cp train1.sh ubuntu-container:/root/train1.sh # copy train script from the host to the container

docker cp train2.sh ubuntu-container:/root/train2.sh # copy train script from the host to the container

 docker exec -it ubuntu-container bash # access container's shell. Go to the home directory and run the training scripts