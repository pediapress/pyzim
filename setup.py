#! /usr/bin/env python

from distutils.core import setup, Extension

ext = Extension(
    '_pyzim',
    ['_pyzim.cpp'],
    language='c++',
    include_dirs=[],
    libraries=['stdc++', 'zim', 'zimwriter'],
    extra_link_args=[],
)

if __name__ == '__main__':
    setup(
        name='pyzim',
        version='0.1',
        py_modules=['pyzim'],
        ext_modules=[ext],
    )
