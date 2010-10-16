#! /usr/bin/env python

from distutils.core import setup, Extension

ext = Extension(
    "pyzim",                 # name of extension
    ["pyzim.cpp"],     # filename of our Cython source
    language="c++",              # this causes Cython to create C++ source
    include_dirs=[],          # usual stuff
    libraries=["stdc++", "zim", "zimwriter"],             # ditto
    extra_link_args=[],       # if needed
    )

if __name__ == '__main__':
    setup(
        name='pyzim',
        version="1.0",
        ext_modules = [ext],
        )
