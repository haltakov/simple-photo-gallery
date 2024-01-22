# Developer Gallery for Testing

This area is used to help with testing and not intended for end users. The
test gallery has several images from Library of Congress "free to use" maritime
collection and are believed to be unencumbered. The images came from here:

https://www.loc.gov/free-to-use/maritime-life/

They are relatively small file size to avoid adding large binaries to the repo.
Over time more photos may be added as additional test cases.

This document contains test procedures and information to help with testing
SPG. Things can change especially with online services so if you find an error
in this document, please open an issue so we can keep this section up to date.

**TOC**

* [Test Procedures](#test-procedures)
    * [Test System Requirements](#test-system-requirements)
    * [Files Gallery](#files-gallery)
    * [Google Photos](#google-photos)
    * [OneDrive Photos](#onedrive-photos)
    * [AWS S3 Upload](#aws-s3-upload)
    * [Netlify Upload](#netlify-upload)
* [Test Setups](#test-setups)
    * [Files Setup](#files-setup)
    * [AWS Setup](#aws-setup)
    * [Netlify Setup](#netlify-setup)
    * [Google Setup](#google-setup)
    * [OneDrive Setup](#onedrive-setup)
* [TODOs](#todos)

## Test Procedures

The following test procedures are all done manually using a makefile and some
scripts. It would be good for this eventually be integrated into CI for at
least some level of automation.

The test procedures utilize a test gallery with some sample images. Python3
virtual environment (venv) is used to always create a clean and reproducible
python environment.

When the venv is created, the current SPG package is installed from source from
the working tree. It is not installed in editable mode so if you make a change
to the source, you need to clean the venv and recreate it. A possible future
change could be to use editable mode instead or create a test option that does.

Using the `venv` also insures that the latest packages from PyPI or whatever is
constrained by the SPG package setup gets installed, and not using whatever
stale versions of packages are on your system. It also makes it easier to catch
breakages due to deprecations and changes in dependent packages.

All of the tests are started from the test directory `examples/test_gallery`.
There is a Makefile there with a little help:

    make help

Make sure you do not already have a python virtual environment activated when
you start a test.

All of the test procedures assume you are starting at the SPG top level and
perform the following steps:

    git switch (branch-being-tested)
    cd examples/test_gallery
    make clean
    make cleanvenv
    make venv
    ...

The branch is whatever branch you want to test and might be master. The clean
steps insure you are starting with everything clean and a predictable
environment. If you are debugging or trying different things it may not be
necessary to clean each time, its up to you.

### Test System Requirements

The following command line tools are needed to run these tests:

* GNU make (or something that can read GNU makefiles)
* expect
* python3 including venv
* bash-like shell (Makefile has some small shell scripts)
* git (if you want to be switching to test branches, etc)

Please create a github issue if there is something I left off the list.

### Files Gallery

The files gallery means that the source of photos are in the local file system
and a static site is generated into the local file system. This is the simplest
situation as it requires no uploads or downloads from third party services.

    git switch (branch-being-tested)        # optional as needed
    cd examples/test_gallery
    make clean
    make cleanvenv
    make venv
    make testinit
    make testbuild

At this point the static site should be built and present at
`output/public/index.html`. You can open this in a browser using `file://` url
to verify the site looks correct. Or you can serve it on `localhost:8008` with
`make serve`.

### Google Photos

This mode builds a static photos site using an album from Google photos as
the source, instead of photos on the local file system. Prior to running this
test you should have set up a Google photo albumm with some test photos and
set it to viewable with URL.

You will need to set an environment variable with the remote URL. A google
remote URL looks like `https://photos.app.goo.gl/n7QTjrKLHruk` (that is a fake
example).

    git switch (branch-being-tested)        # optional as needed
    cd examples/test_gallery
    make clean
    make cleanvenv
    export SPG_REMOTE=(google-album-url)
    make venv
    make testinitrem
    make testbuild

At this point the static site should be built and present at
`output/public/index.html`. You can open this in a browser using `file://` url
to verify the site looks correct. Or you can serve it on `localhost:8008` with
`make serve`.

There will also be a link on the generated static site back to the original
Google photo album.

### OneDrive Photos

At the time of this writing I have not tested OneDrive photos, but it should
be almost the same as Google Photos.

### AWS S3 Upload

Once a static site album has been generated, either from local files or a
remote album, it can be uploaded to a third party host. One of the upload
host options is AWS S3. In order to use this you must have already set up
AWS S3 for static hosting which is beyond the scope of this section. For a
little help see [AWS Setup](#aws-setup).

You will need to set up an environment variable with your S3 bucket URL. This
is your S3 bucket, not the public URL for read access. It looks like
`s3://some-bucket-name`.

    git switch (branch-being-tested)        # optional as needed
    cd examples/test_gallery
    make clean
    make cleanvenv
    export SPG_AWS_BUCKET=(aws-bucket-upload-url)
    make venv
    make testinit
    make testbuild
    make testaws

All the steps prior to `testaws` are the same as [File Gallery](#files-gallery)
and you can verify the local site in the same way.

The `make testaws` step should upload your site to your AWS bucket. You can
then view your static site on AWS using your public read URL for your bucket.

### Netlify Upload

At the time of this writing I have not tested with Netlify.

## Test Setups

Running basic init and build from files does not require any special setup.
But use in AWS or Netlify for uploads, and Google or Onedrive for albums
requires special setups:

### Files Setup

Teting the files-only gallery does not require any setup outside cloning the
repo and meeting the [test system requirements](#test-system-requirements).

### AWS Setup

SPG supports uploading a gallery to AWS S3 as a static web site.
This is a brief high-level overview for testing with AWS. It is not a tutorial
about how to set up AWS and it can be a little complicated.

First, you need an AWS account. Then you have to create an S3 bucket.

Create AWS S3 account https://aws.amazon.com/s3/

Incomplete and not very detailed steps to set up s3:

Create a bucket. Configure it to serve static web site (properties)

You need to create a user that can access the bucket using the aws command
line tool. I could not get the IAM Identity Center to work for setting up a
user and giving permissions. So I gave up and used the deprecated IAM to create
a user.

Once I had the user, added policy in my bucket that looks like this:

```
{
    "Version": "2012-10-17",
    "Id": "Policy1704226183223",
    "Statement": [
        {
            "Sid": "Stmt1704226177122",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::xxxxxxxxx:user/Joe"
            },
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::spg-gallery-test/*"
        },
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::spg-gallery-test/*"
        }
    ]
}
```

I also had to turn off all the "block public access" settings.

You need to install the aws command line tool and configure it. I did this with

    aws configure

and used my access key and secret key from my IAM user. After that you can try

    aws s3 ls

and you should see the name of your bucket

Once I did this, then `gallery-upload aws s3://spg-gallery-test` worked.
I was able to view the gallery at my bucket private URL.

### Netlify Setup

SPG supports uploading a gallery to Netlify for a photos web site.

I have not yet got a test working for netlify at the time of this writing.

### Google Setup

SPG support building a photo gallery from photos in a google photo album.

To test this simply create a small album in google photos and then get the
album sharing URL. That URL can then be used for testing SPG gallery-init
with a google album.

### OneDrive Setup

At the time of this writing I have not tested with OneDrive.

## TODOs

* integrate some or all with CI
* expand expect scripts for something other than default case
* consider editable mode for venv package install
* docker image with test environment
* add tests with different layout configs, ie photos in non-standard location
* review how much of this could be done by python unit tests instead

