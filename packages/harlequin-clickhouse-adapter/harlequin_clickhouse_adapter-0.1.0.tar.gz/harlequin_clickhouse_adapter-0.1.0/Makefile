PYTHON ?= python

.PHONY: clean build publish

clean:
	rm -rf dist build

build: clean
	uv build

publish: build
	uv publish
