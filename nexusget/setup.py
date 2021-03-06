"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup
import py2app
from distutils.core import *
from distutils import sysconfig

APP = ['nxg.py']
PACKAGES= ['h5py']
OPTIONS = {'argv_emulation': False,
           'packages': PACKAGES,
           'excludes': ['scipy', 'matplotlib']}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
