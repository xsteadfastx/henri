.PHONY: all clean init test \
	run \
	formatting \
	rshell \
	sync \
	build-builder push-builder \
	build-esp32 build-esp8266 build-unix \
	erase-flash flash-henri flash-deps flash-plain \
	res \
	submodule-update

init:
	poetry install

test:
	poetry run tox -e unittest

formatting:
	poetry run tox -e formatting

rshell:
	poetry run rshell -p /dev/ttyUSB0

sync:
	poetry run rshell -p /dev/ttyUSB0 rsync -m src/ /pyboard

clean:
	docker volume rm henri-build-temp
	poetry run rshell -p /dev/ttyUSB0 rm -r /pyboard/*

build-builder:
	docker build -f Dockerfile.build -t quay.io/xsteadfastx/henri-builder .

push-builder:
	docker push quay.io/xsteadfastx/henri-builder

build-henri: res
	docker run --rm -ti \
		-v $(PWD):/origin:ro \
		-v $(PWD)/build:/build \
		-e "HENRI=True" -e "DEPS=True" \
		-e "PORT=esp32" \
		quay.io/xsteadfastx/henri-builder \
		sh /origin/.build.sh

build-esp32: res build-henri
	docker run --rm -ti \
		-v $(PWD):/origin:ro \
		-v $(PWD)/build:/build \
		-e "HENRI=False" -e "DEPS=True" \
		-e "PORT=esp32" \
		quay.io/xsteadfastx/henri-builder \
		sh /origin/.build.sh
	docker run --rm -ti \
		-v $(PWD):/origin:ro \
		-v $(PWD)/build:/build \
		-e "HENRI=False" -e "DEPS=False" \
		-e "PORT=esp32" \
		quay.io/xsteadfastx/henri-builder \
		sh /origin/.build.sh

build-esp8266:
	docker run --rm -ti \
		-v $(PWD):/origin:ro \
		-v $(PWD)/build:/build \
		-e "HENRI=False" -e "DEPS=False" \
		-e "PORT=esp8266" \
		quay.io/xsteadfastx/henri-builder \
		sh /origin/.build.sh
	docker run --rm -ti \
		-v $(PWD):/origin:ro \
		-v $(PWD)/build:/build \
		-e "HENRI=False" -e "DEPS=True" \
		-e "PORT=esp8266" \
		quay.io/xsteadfastx/henri-builder \
		sh /origin/.build.sh
	docker run --rm -ti \
		-v $(PWD):/origin:ro \
		-v $(PWD)/build:/build \
		-e "HENRI=True" -e "DEPS=True" \
		-e "PORT=esp8266" \
		quay.io/xsteadfastx/henri-builder \
		sh /origin/.build.sh
build-unix: res
	docker run --rm -ti \
		-v $(PWD):/origin:ro \
		-v $(PWD)/build:/build \
		-v henri-build-temp:/henri/submodules/pycopy/lib \
		-e "HENRI=True" -e "DEPS=True" -e "PORT=unix" \
		quay.io/xsteadfastx/henri-builder \
		sh /origin/.build.sh

all: res build-esp32 build-unix

erase-flash:
	poetry run esptool.py --port /dev/ttyUSB0 erase_flash

flash-henri: erase-flash
	poetry run esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 build/esp32-henri.bin

flash-deps: erase-flash
	poetry run esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 build/esp32-deps.bin

flash-plain: erase-flash
	poetry run esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 build/esp32-plain.bin

run:
	rm src/henri/templates/*_html.py
	build/pycopy -m run

res:
	cd src/henri; ../../submodules/pycopy/tools/mpy_bin2res.py static/css/* >R.py

submodule-update:
	git submodule foreach git remote update
	git submodule foreach 'git reset --hard `git rev-list --max-parents=0 HEAD`'
	git submodule foreach git merge upstream/master
