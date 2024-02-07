Install with Python Virtual Environment
=======================================

(Everything written here assumes you are using python 3).

Using a python virtual environment for installing python programs can help
avoid dependency conflicts and keep your base system clean.

## TLDR

```
cd (my working directory)
python3 -m venv venv
. venv/bin/activate
pip install simple-photo-gallery
...
(use simple photo gallery)
...
deactivate
```

## What is it

When you install a python program using `pip install (some-program)` all the
files for that program get installed on your system somewhere. Usually a
python program also has "dependencies" which are librarites used by the program
that also get installed on your system.

A python virtual environment is a directory that you create somewhere (in your
working directory), and once activated is then used for all installations of
your program and any dependent libraries. Everything goes in this location and
your system level python installation is unaffected.

When you are done you can "deactivate" the virtual environment and even delete
it. When you delete it, then all the installed files are erased and your system
level python is unaffected.

## Why use it

Almost every python program that you install will also install any libraries
that it depends on. Sometimes the program even needs a specific version of a
library. For example, this program `simple-photo-gallery` uses the "requests"
library, and need it to be at least version 2.22.0 or higher.

If you install a lot of python programs on your system, then over time you can
end up with a lot of python libraries installed, and sometimes you even end up
with "version conflicts" where two different programs need different specific
versions of a common library. This is sometimes called
[dependency hell](https://en.wikipedia.org/wiki/Dependency_hell).

When you create a python virtual environment, you are creating a separate area
on your system just for the program you install and all of it's specific
dependencies. When you run the program it uses the libraries from the virtual
environment. When you are done using the program, and want to clean up your
system, you can just delete the virtual environment and all the dependencies
are erased.

Each python program you install can have its own "sandbox". each with different
and even conflicting dependent libraries without interfering with each other.

## Detailed Instructions

There are several ways to create and manage virtual environments with python.
In these instructions we are just using the built-in virtual environment module
that is part of python 3.

The virtual environment will be installed in a directory. One possibility is to
create it in the directory where you will work on your photo gallery. For
example, lets assumes your photos are in a directory named `my_photos`.

Navigate to the photos directory:

    cd my_photos

Create the virtual environment:

    python3 -m venv venv

You will now have a new directory named `venv` under `my_photos`.

Next you need to activate the virtual environment. This step is easy to forget:

    . venv/bin/activate

(That is a dot followed by a space ...)

Once you do this, now every python thing that you do is using the virtual
environment instead of the python installed on your system.

Now just use python like you normally would to insall and use your program:

    pip install simple-photo-gallery

(you might see some warning messages about a newer version of pip. You can
ignore this).

Then you can use simple-photo-gallery as usual:

    gallery-init
    gallery-build
    ...
    (etc)

You can leave the virtual environment active as long as you like. If you close
the command terminal window, then the virtual environment is deactivated. You
can also deactivate it yourself:

    deactivate

After that then you are no longer using the virtual environment. You can always
reactivate it again later:

    cd my_photos
    . venv/bin/activate
    gallery-init
    ...
    (etc)

When you are finally done using simple-photo-gallery for a while and you want
to clean up your disk, you can just delete the venv:

    cd my_photos        # if you are not already in the directory
    deactivate          # if it is activate, need to deactivate
    rm -rf venv         # erases the virtual environment
