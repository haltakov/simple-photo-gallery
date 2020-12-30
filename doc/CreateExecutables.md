# Create Executables

> **NOTE**
> This is still an experimental feature. Please contact me directly if you have any problems with it.

If you want to run the `gallery-init` and `gallery-build` commands without having to install Python, you can use [`pyinstaller`](https://www.pyinstaller.org/) to do that.

1. Install `pyinstaller` using `pip`:
```
pip install pyinstaller
```

2. Checkout or download the code from the [`simple-photo-gallery` repository](https://github.com/haltakov/simple-photo-gallery) on GitHub.

3. Navigate to the root of the `simple-photo-galler` repository.

4. Run the following command to create an executable version of `gallery-init` and all the required data.version

For Linux/MacOS
```
pyinstaller simplegallery/gallery_init.py --add-data simplegallery/data/:simplegallery/data -n gallery-init
```

For Windows:
```
pyinstaller simplegallery\gallery_init.py --add-data simplegallery\data\;simplegallery\data -n gallery-init
```

5. Run the following command to create an executable version of `gallery-build`:

For Linux/MacOS
```
pyinstaller simplegallery/gallery_build.py -n gallery-build
```

For Windows
```
pyinstaller simplegallery\gallery_build.py -n gallery-build
```

6. You can find the binary versions of `gallery-init` and `gallery-build` in the folder `dist`. It contains one folder per command with the executable and all other required files.