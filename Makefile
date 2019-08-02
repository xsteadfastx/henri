.PHONY: all clean init test formatting rshell copy

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
