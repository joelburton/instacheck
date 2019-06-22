all:
	gcc -O2 -o instacheck instacheck.c checks.c -lcrypto

debug:
	gcc -g -O0 -o instacheck instacheck.c checks.c -lcrypto

clean:
	rm -rf instacheck instacheck.dSYM
