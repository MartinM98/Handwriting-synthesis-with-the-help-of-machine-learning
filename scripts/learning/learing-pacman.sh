#!/bin/bash

./../../tesseract-training/hardware-dependent/pacman/train-pacman.sh &

while :
do
	sleep 30m
    if test `find "notification" -mmin +30`
    then
        sendmail -t < test-mail.txt
    fi
done