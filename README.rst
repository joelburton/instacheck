InstaCheck
==========

Check if installation is correct.

Written in Python, but meant to be provided as a .pyc to deter
code examination.

To make::

  $ make

And then provide the made 'instacheck.pyc' to students, to run as
`/usr/bin/python instacheck.pyc`

**Note:** this is intentionally a Python 2 program, since that is
the only version consistently shipped with OSX. The makefile makes
a PYC file that is Py2 specific and only useable by Py2.
