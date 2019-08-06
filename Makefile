.PHONY: all clean init test formatting rshell copy build-firmware

init:
	poetry install

test:
	poetry run tox

formatting:
	poetry run tox -e formatting

rshell:
	poetry run rshell -p /dev/ttyUSB0

copy:
	# poetry run rshell -p /dev/ttyUSB0 cp -r src/* /pyboard/
	poetry run rshell -p /dev/ttyUSB0 rsync -m src/ /pyboard

clean:
	poetry run rshell -p /dev/ttyUSB0 rm -r /pyboard/*

build-builder:
	docker build -f Dockerfile.build -t henri-builder .

build-firmware:
	docker run --rm -ti -v $(PWD):/origin:ro -v $(PWD)/build:/build henri-builder sh /origin/build.sh
