#!/bin/sh
set -ex

# make a copy of the mounted original henri code
sudo cp -Rv /origin /henri

# chown some dirs
sudo chown -R builder /henri
sudo chown -R builder /build

# freeze modules
## pkg_resources
ln -s /henri/src/lib/pkg_resources.py /henri/submodules/pycopy/ports/esp32/modules/pkg_resources.py
## uasyncio
mkdir /henri/submodules/pycopy/ports/esp32/modules/uasyncio
ln -s /henri/src/lib/uasyncio/__init__.py /henri/submodules/pycopy/ports/esp32/modules/uasyncio/__init__.py
ln -s /henri/src/lib/uasyncio/core.py /henri/submodules/pycopy/ports/esp32/modules/uasyncio/core.py
## picoweb
mkdir /henri/submodules/pycopy/ports/esp32/modules/picoweb
ln -s /henri/src/lib/picoweb/__init__.py /henri/submodules/pycopy/ports/esp32/modules/picoweb/__init__.py
ln -s /henri/src/lib/picoweb/utils.py /henri/submodules/pycopy/ports/esp32/modules/picoweb/utils.py
## ulogging
ln -s /henri/src/lib/ulogging.py /henri/submodules/pycopy/ports/esp32/modules/ulogging.py
## henri
if [ "${HENRI}" = "True" ]; then
        ln -s /henri/src/henri.py /henri/submodules/pycopy/ports/esp32/modules/henri.py
fi

# change to pycopy dir
cd /henri/submodules/pycopy

# clone some deps
git submodule update --init lib/berkeley-db-1.xx

# do the compiling
make -j4 -C mpy-cross
make -j4 -C ports/esp32 ESPIDF=/opt/esp-idf

# copy firmware out of the container
cp ports/esp32/build/firmware.bin /build/firmware.bin
