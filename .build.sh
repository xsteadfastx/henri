#!/bin/sh
set -ex

# make a copy of the mounted original =enri code
sudo rsync -av /origin/ /henri

# chown some dirs
sudo chown -R builder /henri
sudo chown -R builder /build

# freeze modules
if [ "${DEPS}" = "True" ]; then
        # pkg_resources
        ln -s \
                /henri/submodules/pycopy-lib/pkg_resources/pkg_resources.py \
                /henri/submodules/pycopy/ports/"${PORT}"/modules/pkg_resources.py

        # uasyncio
        ln -s \
                /henri/submodules/pycopy-lib/uasyncio/uasyncio \
                /henri/submodules/pycopy/ports/"${PORT}"/modules/uasyncio
        ln -s \
                /henri/submodules/pycopy-lib/uasyncio.core/uasyncio/core.py \
                /henri/submodules/pycopy/ports/"${PORT}"/modules/uasyncio/core.py

        # picoweb
        ln -s \
                /henri/submodules/picoweb/picoweb \
                /henri/submodules/pycopy/ports/"${PORT}"/modules/picoweb

        # ulogging
        ln -s \
                /henri/submodules/pycopy-lib/ulogging/ulogging.py \
                /henri/submodules/pycopy/ports/"${PORT}"/modules/ulogging.py

        # random
        ln -s \
                /henri/submodules/pycopy-lib/random/random.py \
                /henri/submodules/pycopy/ports/"${PORT}"/modules/random.py

        # for unix port
        if [ "${PORT}" = "unix" ]; then
                # unittest
                ln -s \
                        /henri/submodules/pycopy-lib/unittest/unittest.py \
                        /henri/submodules/pycopy/ports/"${PORT}"/modules/unittest.py
       fi
fi
## henri
if [ "${HENRI}" = "True" ]; then
        ln -s /henri/src/henri.py /henri/submodules/pycopy/ports/"${PORT}"/modules/henri.py
        ln -s /henri/src/main.py /henri/submodules/pycopy/ports/"${PORT}"/modules/main.py
fi

# remove some uneeded modules
if [ "${PORT}" = "esp32" ]; then
        rm /henri/submodules/pycopy/ports/"${PORT}"/modules/neopixel.py
        rm /henri/submodules/pycopy/ports/"${PORT}"/modules/upip.py
        rm /henri/submodules/pycopy/ports/"${PORT}"/modules/upip_utarfile.py
        rm /henri/submodules/pycopy/ports/"${PORT}"/modules/urequests.py
        rm /henri/submodules/pycopy/ports/"${PORT}"/modules/webrepl.py
        rm /henri/submodules/pycopy/ports/"${PORT}"/modules/webrepl_setup.py
        rm /henri/submodules/pycopy/ports/"${PORT}"/modules/websocket_helper.py
fi

# change to pycopy dir
cd /henri/submodules/pycopy

# do the compiling and copying
make -j4 -C mpy-cross

if [ "${PORT}" = "esp32" ]; then
        # clone some deps
        git submodule update --init lib/berkeley-db-1.xx

        # compile
        make -j4 -C ports/"${PORT}" ESPIDF=/opt/esp-idf

        # copy firmware out of the container
        if [ "${HENRI}" = "True" ] && [ "${DEPS}" = "True" ]; then
                FILENAME="firmware-henri.bin"
        elif [ "${HENRI}" = "False" ] && [ "${DEPS}" = "True" ]; then
                FILENAME="firmware-deps.bin"
        elif [ "${HENRI}" = "False" ] && [ "${DEPS}" = "False" ]; then
                FILENAME="firmware.bin"
        fi
        cp ports/"${PORT}"/build/firmware.bin "/build/$FILENAME"
elif [ "${PORT}" = "unix" ]; then
        make -j4 -C ports/"${PORT}" axtls
        make -j4 -C ports/"${PORT}"
        cp ports/"${PORT}"/pycopy /build/pycopy
fi
