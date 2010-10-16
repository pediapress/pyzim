all:: pyzim.so

pyzim.cpp: pyzim.pyx
	cython --cplus pyzim.pyx

pyzim.so: pyzim.cpp pyas.h
	python setup.py build_ext -f -i

clean::
	rm -rf build *.so
