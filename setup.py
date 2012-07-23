#! /usr/bin/env python

import os
from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext as _build_ext
from distutils.command.sdist import sdist as _sdist
from distutils.util import strtobool

EMBED = strtobool(os.environ.get("EMBED", "1"))


def get_version():
    d = {}
    try:
        execfile("pyzim.py", d, d)
    except (ImportError, RuntimeError):
        pass
    return d["__version__"]


class sdist(_sdist):
    def run(self):
        if os.path.exists("Makefile"):
            os.system("make _pyzim.cpp")
        _sdist.run(self)


class build_ext(_build_ext):
    def run(self):
        if os.path.exists("Makefile"):
            os.system("make _pyzim.cpp")

        if EMBED and os.path.exists("vendor/Makefile"):
            target = os.environ.get("PP_TARGET", "all")
            bdir = os.path.abspath(self.build_temp)
            os.environ["BUILD"] = bdir
            if "MAKE" not in os.environ:
                os.environ["MAKE"] = "make"
            err = os.system("cd vendor; $MAKE -j1 %s" % target)
            assert err == 0, "make failed"
            if self.include_dirs is None:
                self.include_dirs = []
            self.include_dirs.insert(0, os.path.join(bdir, "prefix", "include"))

            if self.library_dirs is None:
                self.library_dirs = []
            self.library_dirs.insert(0, os.path.join(bdir, "prefix", "lib"))

        _build_ext.run(self)

ext = Extension(
    '_pyzim',
    ['_pyzim.cpp'],
    language='c++',
    include_dirs=[],
    libraries=["zimwriter", "zim", "cxxtools", "lzma", "stdc++"],
    extra_link_args=[])

if __name__ == '__main__':
    setup(
        name='pyzim',
        version=get_version(),
        py_modules=['pyzim'],
        ext_modules=[ext],
        maintainer="pediapress.com",
        maintainer_email="info@pediapress.com",
        url="https://github.com/pediapress/pyzim",
        cmdclass=dict(build_ext=build_ext, sdist=sdist))
