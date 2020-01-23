from setuptools import setup, find_packages
import os

current_folder = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_folder, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Simple Photo Gallery',
    version='0.1.1',
    description='Create and share simple, but beautiful photo galleries, you are hosing yourself.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/haltakov/simple-photo-gallery',
    author='Vladimir Haltakov',
    author_email='vladimir.haltakov@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='photo video gallery self-hosted html',
    packages=find_packages(),
    python_requires='>=3.6',
    project_urls={
        'Documentation': r'https://github.com/haltakov/simple-photo-gallery'
    },
    package_data={
        'simplegallery' : ['templates/html/*',
                           'templates/public/*']
    }
)
