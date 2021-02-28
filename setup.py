from setuptools import setup, find_packages
import os

current_folder = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_folder, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='simple-photo-gallery',
    version='1.5.0',
    description='Pretty and simple HTML photo galleries you can host yourself.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.haltakov.net/simple-photo-gallery',
    author='Vladimir Haltakov',
    author_email='vladimir.haltakov@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords='photo video gallery self-hosted html',
    packages=find_packages(),
    python_requires='>=3.6',
    project_urls={
        'Documentation': r'https://www.haltakov.net/simple-photo-gallery'
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "gallery-init=simplegallery.gallery_init:main",
            "gallery-build=simplegallery.gallery_build:main",
            "gallery-upload=simplegallery.gallery_upload:main",
        ]
    },
    install_requires=[
        'opencv-python>=4.2.0.32',
        'pillow>=7.0.0',
        'jinja2>=2.10.3',
        'selenium>=3.141.0',
        'requests>=2.22.0',
    ]
)
