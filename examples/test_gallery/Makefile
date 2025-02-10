#
# SPDX-License-Identifier: MIT
#
# Copyright 2023 Joseph Kroesche
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# This Makefile and test photo images are used by developers to help with
# testing and not intended for end-user.
#
# General sequence
#     make testinit
#     make testbuild
#     (from here you can examine generated album for correctness)
#     make testaws (to test upload to s3 you will need aws setup, see README)
#
#     (before running test sequence)
#     make clean (to remove all prior test generated products)
#
# To check remote albums, like google photos or onedrive, set SPG_REMOTE to
# your remote link, then:
#
#     make testinitrem
#     make testbuild
#
# Optional ways to run it:
#
#     export SPG_REMOTE="my_remote_url"
#     make testinitrem
#
#     OR
#
#     SPG_REMOTE="my_remote_url" make testinitrem
#
#     OR
#
#     make testinitrem SPG_REMOTE="my_remote_url"
#
# About python virtual environment:
# This Makefile uses python3 virtual environment (venv) to install everything
# needed for the test so it does not modify any python installations on your
# system. It assumes `python3` is available on your PATH.
# To help manage the venv, there are a couple of targets:
#
#     make venv (will create the venv and nothing else)
#     make cleanvenv (will remove the venv)
#
# Note that the `testinit*` targets will automatically create the venv if it
# does not already exist. So you dont need to explicity `make venv` but I like
# to do that to keep steps separated.
# When you are finished test you can `make cleanvenv` to clean up your system.
# Also, I like to start with fresh venv because then you will get the latest
# packages from PyPI that are not already constrained by this package setup.py
# and it can uncover problems when dependencies are updated that introduce
# breakages.

# temp dir where source files and generated site will be located. it can be
# safely deleted
TESTDIR=output

# port for local serving the static site. using 8008 because 8000 gets a little
# overcrowded on my system
SERVER_PORT=8008

all: help

.PHONY: help
help:
	@echo ""
	@echo "Makefile help"
	@echo "-------------"
	@echo ""
	@echo "testinit    - test creation of gallery from files (gallery-init)"
	@echo "testinitrem - test init of gallery from remote album (goog or onedrive)"
	@echo "              (need to set SPG_REMOTE variable)"
	@echo "              (current setting SPG_REMOTE=$(SPG_REMOTE))"
	@echo "testbuild   - test build of gallery (gallery-build)"
	@echo "testaws     - test upload to aws (gallery-upload aws)"
	@echo "              (need to set SPG_AWS_BUCKET)"
	@echo "              (current setting SPG_AWS_BUCKET=$(SPG_AWS_BUCKET))"
	@echo "clean       - clean generated files"
	@echo "serve       - run local python web server for static site"
	@echo ""
	@echo "venv        - create python virtual environment (automatic when needed)"
	@echo "venvdist    - use dist package instead of source (SPG_VER=$(SPG_VER))"
	@echo "cleanvenv   - clean the python venv"
	@echo "safety      - run python package checker (automatic when needed)"
	@echo ""

$(TESTDIR):
	cp -r src_photos/ $@

.PHONY: testinit
testinit: venv $(TESTDIR)
	. venv/bin/activate; cd $(TESTDIR); expect ../init.expect

# in this case we dont want any pre-populated photos in the temp dir
.PHONY: testinitrem
testinitrem: venv clean
	mkdir $(TESTDIR)
	. venv/bin/activate; cd $(TESTDIR); expect ../initrem.expect "$(SPG_REMOTE)"

.PHONY: testbuild
testbuild: $(TESTDIR)/public/index.html

.PHONY: testaws
testaws:
	. venv/bin/activate; cd $(TESTDIR); gallery-upload aws $(SPG_AWS_BUCKET)

.PHONY: testnetlify
testnetlify:
	. venv/bin/activate; cd $(TESTDIR); gallery-upload netlify

$(TESTDIR)/public/index.html:
	. venv/bin/activate; cd $(TESTDIR); gallery-build

.PHONY: clean
clean:
	rm -rf $(TESTDIR)

.PHONY: serve
serve: venv
	venv/bin/python -m http.server -d $(TESTDIR)/public $(SERVER_PORT)

venv: venv/bin/activate
	venv/bin/python -m pip install ../..
	venv/bin/safety check

.PHONY: venvdist
venvdist: venv/bin/activate
	venv/bin/python -m pip install ../../dist/simple_photo_gallery-$(SPG_VER)-py3-none-any.whl
	venv/bin/safety check

venv/bin/activate:
	test -d venv || python3 -m venv venv
	touch $@
	venv/bin/python -m pip install -U pip setuptools wheel
	venv/bin/python -m pip install -U safety
	touch venv

.PHONY: cleanvenv
cleanvenv:
	rm -rf venv

.PHONY: safety
safety: venv
	venv/bin/safety check
