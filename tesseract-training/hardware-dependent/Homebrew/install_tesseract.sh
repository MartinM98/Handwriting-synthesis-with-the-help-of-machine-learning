#!/bin/bash
# https://tesseract-ocr.github.io/tessdoc/Compiling.html


brew install automake autoconf libtool
brew install pkgconfig
brew install icu4c
brew install leptonica
brew install pango
brew install libarchive
brew install gcc

git clone https://github.com/tesseract-ocr/tesseract/
cd tesseract
./autogen.sh
mkdir build
cd build
# Optionally add CXX=g++-8 to the configure command if you really want to use a different compiler.
../configure PKG_CONFIG_PATH=/usr/local/opt/icu4c/lib/pkgconfig:/usr/local/opt/libarchive/lib/pkgconfig:/usr/local/opt/libffi/lib/pkgconfig
make -j
# Optionally install Tesseract.
sudo make install
# Optionally build and install training tools.
make training
sudo make training-install

sudo wget https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata -P /usr/local/share/tessdata/

#brew install tesseract # install tesseract