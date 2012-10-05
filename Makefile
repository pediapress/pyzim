all:: _pyzim.so

_pyzim.cpp: _pyzim.pyx
	cython --cplus _pyzim.pyx

_pyzim.so: _pyzim.cpp pyas.h
	python setup.py build_ext -f -i

clean::
	rm -rf build _pyzim.so _pyzim.cpp
