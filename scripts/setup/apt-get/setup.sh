#install ssmtp - email notifiactions
# echo "Installing ssmtp - START"
# git clone https://aur.archlinux.org/ssmtp.git
# # tar zxvf ssmtp.tar.gz
# cd ssmtp
# makepkg -sri
# cd ..
# sudo rm -R ssmtp
# echo "Installing ssmtp - END"

#configure email notification system
echo "Configuring email notification system - START"
sudo rm  -f /etc/ssmtp/revaliases
sudo cp ../revaliases /etc/ssmtp/revaliases
sudo rm  -f /etc/ssmtp/ssmtp.conf
sudo cp ../ssmtp.conf /etc/ssmtp/ssmtp.conf
echo "Configuring email notification system  - END"

#install tesseract
echo "Installing tesseract  - START"
./../../tesseract-training/hardware-dependent/apt-get/install_tesseract.sh
echo "Installing tesseract   - END"

# download dataset