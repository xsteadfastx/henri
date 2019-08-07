.PHONY: all clean init test formatting rshell sync build-builder build-henri-firmware build-deps-firmware build-plain-firmware flash erase-flash flash-henri flash-deps flash-plain

init:
	poetry install

test:
	poetry run tox

formatting:
	poetry run tox -e formatting

rshell:
	poetry run rshell -p /dev/ttyUSB0

sync:
	poetry run rshell -p /dev/ttyUSB0 rsync -m src/ /pyboard

clean:
	poetry run rshell -p /dev/ttyUSB0 rm -r /pyboard/*

build-builder:
	docker build -f Dockerfile.build -t henri-builder .

build-henri-firmware:
	docker run --rm -ti -v $(PWD):/origin:ro -v $(PWD)/build:/build -e "HENRI=True" -e "DEPS=True" henri-builder sh /origin/build.sh

build-deps-firmware:
	docker run --rm -ti -v $(PWD):/origin:ro -v $(PWD)/build:/build -e "HENRI=False" -e "DEPS=True" henri-builder sh /origin/build.sh

build-plain-firmware:
	docker run --rm -ti -v $(PWD):/origin:ro -v $(PWD)/build:/build -e "HENRI=False" -e "DEPS=False" henri-builder sh /origin/build.sh

all: build-henri-firmware build-deps-firmware build-plain-firmware

erase-flash:
	poetry run esptool.py --port /dev/ttyUSB0 erase_flash

flash-henri: erase-flash
	poetry run esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 build/firmware-henri.bin

flash-deps: erase-flash
	poetry run esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 build/firmware-deps.bin

flash-plain: erase-flash
	poetry run esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 build/firmware-plain.bin
