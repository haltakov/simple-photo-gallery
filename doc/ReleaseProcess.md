# Release Process Notes for Developers

This is a manual process for now. This should be automated.

Also, this procedure could be refactored to reduce the amount of switching
between virtual environments.

## Preconditions

1. All issues intended to be fixed in this release have been completed.
2. Everything needed has been committed and pushed and `master` is clean.
3. All CI tests pass.
4. You have done a preliminary release and tested it and have high confidence
   it is ready for release. (do build and test as described below)
5. Make sure you are not in an activated venv: `deactivate`
6. If there already exists a `venv` directory in project root, remove it:
   `rm -rf venv`

## Versioning

1. Increment the version number in `setup.py`.
2. Commit setup.py, commit to master branch and push.
3. `git tag 1.2.3` (optional - see notes)
4. `git push origin 1.2.3` (see notes)

**Tag notes:**

* Instead of tagging using command line git in your local repo, you can instead
  do it from Github UI. If you prefer that, then see the Publish section below.
* If, after tagging you make further commits before releasing, be sure to move
  the tag to be the most recent commit at the time of release.

## Setup

1. In the project root, create a venv and activate
2. install `twine`
3. Install `build`

```
cd simple-photo-gallery     # project root
python3 -m venv venv
. venv/bin/activate
pip install twine
pip install build
```

## Build

Create wheel and source distributions:

1. ensure you are in project root directory
2. virtual environment is activated
3. `python3 -m build --sdist`
4. `python3 -m build --wheel`

You will now have a source and wheel package in the `./dist` directory.

## Test

### Unit Tests

Run the unit tests located in `simplegallery/test`.

1. Create venv in the project root as described above in **Setup**
2. Make sure the venv is activated: `. venv/bin/activate`
3. Install packages from `requirements.txt`: `pip install -r requirements.txt`
4. From project root, run the unit tests:

    python -m unittest simplegallery/test/*.py

This will generate a lot of output. Usually it is obvious if a test fails. Scan
the console output to make sure all the test ran okay.

### Integration Test

The integration test will use a clean venv and install the distribution package
you built earlier, and run some tests against it.

1. Deactivate the previous venv: `deactivate`
2. Switch to the test gallery directory: `cd examples/test_gallery`
3. Set the version of the package you are testing: `export SPG_VER=1.2.3`
4. `make help` to verify that the version is correct (the help text will show
   the value for `venvdist`)
5. Create the test venv, but using the distribution package instead of the
   default: `make venvdist`

Now you have created a venv using the SPG distribution package. This is the
same package that will be published on PyPI, assuming all tests are okay. Run
tests as described in the [Test Gallery README](../examples/test_gallery/README.md).

Here is the short version that does not include any remote galleries or
deployment tests. This is an example to show the process of setting up and
running some tests, but probably you should do more than this for a release:

```
deactivate              # make sure no other venv is active
cd examples/test_gallery
export SPG_VER=1.2.3    # use the actual version, obviously
make clean              # clean out old tests
make cleanvenv
make venvdist
make testinit
make testbuild
```

There should be no error messages generated. Examine the static gallery under
`output/public`.

You can also open `output/public/index.html` with a browser to verify the
generated site. Or instead `make serve` and open a browser to
`http://localhost:8008`.

## Publish

At this stage everything above should be done:

* the version in `setup.py` was updated
* built packages with the new version in the `dist` directory
* committed (and pushed) the updated `setup.py`
* HEAD commit is tagged with the version (and the tag is pushed)
* testing was done and you are satisfied with test result

### Github Release

**Note:** before you start, it is a good idea to create a temporary text file
with the release notes. Look at the commit history to see all the changes that
were made, and make a list of bugs (issue numbers) that were fixed. This will
make it easier when you get to the step below for filling out the release
description.

Create a release on github from the new version tag you pushed (assumes you
are a maintainer of this project on github):

1. https://github.com/haltakov/simple-photo-gallery
2. go to the releases page
3. click "draft a new release"
4. under the "choose a tag" dropdown, you can select the tag you creeated
   earlier, or if you did not create one already you can create a new tag here.
   (if you create a new tag it should be of the form 1.2.3)
5. for title, enter "Release v1.2.3" (except use the actual version number)
6. In the description box, type up the release notes. This should summarize
   changes in the release, any new feature, bugs fixed, etc. (paste the release
   notes you created earlier)
7. use the preview tab to see what the release notes will look like
8. if you are satisfied, check "set as latest release" and click "Publish"
9. go to the releases page and make sure the new release looks good

### PyPI

Make sure that any previous venv is deactivated, and that you are in the
project root directory.

The following assumes that you have an account on PyPI and are a maintainer of
this project. You will also need your API token.

**Note:** at the upload step, you will be asked for credentials. Use the
following credentials:

* username: `__token__`
* password: you API token, including the `pypi-` prefix

```
cd simple-photo-gallery # go to project root directory
deactivate              # if a venv was activated
. venv/bin/activate     # activate the venv you created earlier
twine upload dist/*
```

After upload is complete, examine project on PyPI to make sure it looks good.

### Wrapup

On Github, close any issues for this release that are still open. Add closing
comments if appropriate. If you are using milestones, close the milestone.
