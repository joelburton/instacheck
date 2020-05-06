all:
	#gcc -O2 -o instacheck instacheck.c checks.c /usr/lib/libcrypto.dylib
	/usr/bin/python -c "__import__('instacheck')"

clean:
	rm instacheck.pyc
