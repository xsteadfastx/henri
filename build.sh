#!/bin/sh
set -ex

# make a copy of the mounted original henri code
sudo cp -Rv /origin /henri

# chown some dirs
sudo chown -R builder /henri
sudo chown -R builder /build

# freeze modules
if [ "${DEPS}" = "True" ]; then
        ## pkg_resources
        ln -s /henri/submodules/pycopy-lib/pkg_resources/pkg_resources.py /henri/submodules/pycopy/ports/esp32/modules/pkg_resources.py
        ## uasyncio
        ln -s /henri/submodules/pycopy-lib/uasyncio/uasyncio /henri/submodules/pycopy/ports/esp32/modules/uasyncio
        ln -s /henri/submodules/pycopy-lib/uasyncio.core/uasyncio/core.py /henri/submodules/pycopy/ports/esp32/modules/uasyncio/core.py
        ## picoweb
        ln -s /henri/submodules/picoweb/picoweb /henri/submodules/pycopy/ports/esp32/modules/picoweb
        ## ulogging
        ln -s /henri/submodules/pycopy-lib/ulogging/ulogging.py /henri/submodules/pycopy/ports/esp32/modules/ulogging.py
fi
## henri
if [ "${HENRI}" = "True" ]; then
        ln -s /henri/src/henri.py /henri/submodules/pycopy/ports/esp32/modules/henri.py
        ln -s /henri/src/main.py /henri/submodules/pycopy/ports/esp32/modules/main.py
fi

# remove some uneeded modules
rm /henri/submodules/pycopy/ports/esp32/modules/neopixel.py
rm /henri/submodules/pycopy/ports/esp32/modules/upip.py
rm /henri/submodules/pycopy/ports/esp32/modules/upip_utarfile.py
rm /henri/submodules/pycopy/ports/esp32/modules/urequests.py
rm /henri/submodules/pycopy/ports/esp32/modules/webrepl.py
rm /henri/submodules/pycopy/ports/esp32/modules/webrepl_setup.py
rm /henri/submodules/pycopy/ports/esp32/modules/websocket_helper.py

# change to pycopy dir
cd /henri/submodules/pycopy

# clone some deps
git submodule update --init lib/berkeley-db-1.xx

# do the compiling
make -j4 -C mpy-cross
make -j4 -C ports/esp32 ESPIDF=/opt/esp-idf

# copy firmware out of the container
if [ "${HENRI}" = "True" ] && [ "${DEPS}" = "True" ]; then
        FILENAME="firmware-henri.bin"
elif [ "${HENRI}" = "False" ] && [ "${DEPS}" = "True" ]; then
        FILENAME="firmware-deps.bin"
elif [ "${HENRI}" = "False" ] && [ "${DEPS}" = "False" ]; then
        FILENAME="firmware.bin"
fi
cp ports/esp32/build/firmware.bin "/build/$FILENAME"
