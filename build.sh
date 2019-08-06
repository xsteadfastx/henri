#!/bin/sh
set -ex
sudo cp -Rv /origin /henri
sudo chown -R builder /henri
mkdir /henri/submodules/pycopy/ports/esp32/modules/picoweb
ln -s /henri/src/lib/picoweb/__init__.py /henri/submodules/pycopy/ports/esp32/modules/picoweb/__init__.py
ln -s /henri/src/lib/picoweb/utils.py /henri/submodules/pycopy/ports/esp32/modules/picoweb/utils.py
ln -s /henri/src/main.py /henri/submodules/pycopy/ports/esp32/modules/main.py
cd /henri/submodules/pycopy
git submodule update --init lib/berkeley-db-1.xx
make -j4 -C mpy-cross
make -j4 -C ports/esp32 ESPIDF=/opt/esp-idf
ls -la ports/esp32/build
