"""Confirm Rithm setup instruction was successful."""

import sys
import os
import re
import subprocess

def do_checks():
    
    # xcode

    if not cmd_match(
        "xcode-select -p", 
        "^/Applications/Xcode.app/Contents/Developer" ):
        err("Xcode not installed")
        ok = False

    # homebrew itself

    if not cmd_match(
        "which brew",
        "^/usr/local/bin/brew$" ):
        err("Homebrew not installed")
        ok = False

    # python version & not in a venv

    if not cmd_match(
        "which python3", 
        "^/usr/local/bin/python3$"):
        err("Python not installed properly")
        ok = False

    if not cmd_match(
        "which ipython", 
        "^/usr/local/bin/ipython$"):
        err("IPython not installed properly")
        ok = False

    # node + npm

    if not cmd_match(
        "which npm", 
        "^/usr/local/bin/npm$"):
        err("NPM not installed properly")
        ok = False
    
    if not cmd_match(
        "node -v", 
        "^v12."):
        err("Wrong node version")
        ok = False

    # postgresql

    if not cmd_match(
        "which psql", 
        "^/usr/local/bin/psql$"):
        err("PostgreSQL not installed correctly")
        ok = False

    if not cmd_match(
        "psql -V", 
        r"^psql .* 12"):
        err("Wrong PostgreSQL version")
        ok = False

    # vscode

    if not cmd_match(
        "which code", 
        "^/usr/local/bin/code$"):
        err("VSCode not installed or 'code' command not set up")
        ok = False

    # heroku

    if not cmd_match(
        "which heroku",
        "^/usr/local/bin/heroku$"):
        err("Heroku not installed")
        ok = False

    # tree

    if not cmd_match(
        "which tree", 
        "^/usr/local/bin/tree$"):
        err("Tree not installed properly")
        ok = False

    # bash

    if not env_match("SHELL", "^/usr/local/bin/bash$"):
        err("Not using right bash as your shell")
        ok = False

    # our bash profile stuff

    if not env_match("FLASK_ENV", "^development$"):
        err("Wrong or missing $FLASK_ENV; did you get our bash setup?")
        ok = False

    # git setup

    if not file_match(
        os.path.expanduser("~/.gitconfig"), 
        ".gitignore_global"):
        err(".gitconfig is not set up with our commands")
        ok = False

        if not file_match(
            os.path.expanduser("~/.gitignore_global"),
            "venv"):
            err(".gitignore_global does not contain our contents")

    return ok


### HERE BE DRAGONS --- SHOULDN'T NEED TO CHANGE THIS STUFF

verbose = False

def err(msg):
    print("*** ERROR: %s" % msg)

def regex_match(pattern, string):    
    result = re.search(pattern, string)
    if verbose:
        print("%s %s ~ %s" % (
            "match" if result else "nomatch",
            pattern, 
            string, 
        ))
    return result

def cmd_match(cmd, pattern):
    try:
        rez = (subprocess
                .check_output(cmd, shell=True)
                .strip()
                .decode('utf8'))
    except subprocess.CalledProcessError as err:
        if verbose:
            print("  cmderr = %s" % err)
    else: 
        return regex_match(pattern, rez)

def env_match(envname, pattern):
    return regex_match(pattern, os.environ.get(envname, ""))

def file_match(path, pattern):
    try:
        with open(path) as f:
            return regex_match(pattern, f.read())
    except Exception as err:
        if verbose:
            print("  fileerr = %s" % err)

def main():
    global verbose

    verbose = len(sys.argv) > 1 and sys.argv[1] == "-v"
    ok = do_checks()

    if not ok:
        print("""
*** YOU HAVE ERRORS:
    Check installation instructions carefully and follow every step.
    Need help? Run again as 'python instacheck -v' and submit that output. 
""")
        sys.exit(1)

    print("""
*** EVERY CHECK SUCCESSFUL
    Congratulations! Please send us the following line:
""")

    # signature
    username = os.environ["USER"]
    sig = subprocess.check_output(
        "echo '%s' | shasum" % username, shell=True)
    print("  %s = %s\n" % (username, sig))


if __name__ == "__main__":
    main()