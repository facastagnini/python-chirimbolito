"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='chirimbolito',
    version='0.dev6', # Single digit based release NN
    description='A Bitcoin address monitoring tool built with a Raspberry Pi and a LCD display',
    long_description=long_description,
    url='https://github.com/facastagnini/python-chirimbolito',
    author='Federico Ariel Castagnini',
    author_email='federico.castagnini@protonmail.com',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='raspberry pi rpi bitcoin lcd wallet monitoring',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # install sample config file
    data_files=[
        (path.join(path.expanduser('~'), '.config'), ['chirimbolito.json'])
    ],

    # remove future after https://github.com/debrouwere/python-ballpark/pull/5
    # remove pandas after https://github.com/debrouwere/python-ballpark/pull/6
    install_requires=['Adafruit_CharLCD', 'RPi.GPIO','requests','ballpark','future','pandas'],
    entry_points={
        'console_scripts': [
            'chirimbolito = chirimbolito.Chirimbolito:run',
        ],
    },
)

