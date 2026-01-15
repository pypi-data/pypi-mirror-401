PYTHON ?= python

.PHONY: clean build test publish

clean:
	rm -rf dist build

build: clean
	uv build

test:
	uv run pytest

publish: build
	uv publish
