.PHONY: all clean init test formatting rshell copy build-builder build-henri-firmware build-plain-firmware flash

init:
	poetry install

test:
	poetry run tox

formatting:
	poetry run tox -e formatting

rshell:
	poetry run rshell -p /dev/ttyUSB0

copy:
	poetry run rshell -p /dev/ttyUSB0 rsync -m src/ /pyboard

clean:
	poetry run rshell -p /dev/ttyUSB0 rm -r /pyboard/*

build-builder:
	docker build -f Dockerfile.build -t henri-builder .

build-henri-firmware:
	docker run --rm -ti -v $(PWD):/origin:ro -v $(PWD)/build:/build -e "HENRI=True" henri-builder sh /origin/build.sh

build-plain-firmware:
	docker run --rm -ti -v $(PWD):/origin:ro -v $(PWD)/build:/build -e "HENRI=False" henri-builder sh /origin/build.sh

flash:
	poetry run esptool.py --port /dev/ttyUSB0 erase_flash
	poetry run esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 build/firmware.bin
