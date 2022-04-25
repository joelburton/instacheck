"""Confirm Rithm setup instruction was successful."""

import sys
import os
import re
import subprocess


def chk_xcode():
    cmd_match(
        "xcode-select -p",
        "^/Applications/Xcode.app/Contents/Developer",
        "Xcode not installed")


def chk_homebrew():
    cmd_match(
        "which brew",
        "^(/usr/local/bin/brew|/opt/homebrew/bin/brew)$",
        "Homebrew not installed")


def chk_zsh():
    cmd_match(
        "which zsh",
        "^/bin/zsh$",
        "Correct zsh not being used")


def chk_python():
    cmd_match(
        "which python3",
        "^(/opt/homebrew/bin/python3|/usr/local/bin/python3)$",
        "Python not installed properly")

    cmd_match(
        "which ipython",
        "^(/opt/homebrew/bin/ipython|/usr/local/bin/ipython)$",
        "IPython not installed properly")


def chk_postgres():
    cmd_match(
        "which psql",
        "^(/opt/homebrew/bin/psql|/usr/local/bin/psql)$",
        "PostgreSQL not installed correctly")

    cmd_match(
        "psql -V",
        r"^psql .* 14",
        "Wrong PostgreSQL version")


def chk_git():
    file_match(
        os.path.expanduser("~/.gitconfig"),
        ".gitignore_global",
        ".gitconfig is not set up with our commands")

    file_match(
        os.path.expanduser("~/.gitignore_global"),
        "venv",
        ".gitignore_global does not contain our contents")


def chk_node():
    cmd_match(
        "which npm",
        "^(/opt/homebrew/bin/npm|/usr/local/bin/npm)$",
        "NPM not installed properly")

    cmd_match(
        "node -v",
        "^v18.",
        "Wrong node version")

    cmd_match(
        "nodemon -v",
        "^2",
        "Nodemon not properly installed")


def chk_shell():
    cmd_match(
        "which tree",
        "^(/opt/homebrew/bin/tree|/usr/local/bin/tree)$",
        "Tree not installed properly")


def chk_heroku():
    cmd_match(
        "which heroku",
        "^(/opt/homebrew/bin/heroku|/usr/local/bin/heroku)$",
        "Heroku not installed")


def chk_insomnia():
    cmd_match(
        "ls -d /Applications/Insomnia.app",
        "/Applications/Insomnia.app",
        "Insomnia not installed")


def chk_vscode():
    cmd_match(
        "which code",
        "^(/opt/homebrew/bin/code|/usr/local/bin/code)$",
        "VSCode not installed or 'code' command not set up")


def chk_env():
    env_match(
        "FLASK_ENV",
        "^development$",
        "Wrong or missing $FLASK_ENV; did you get our bash setup?")


MACOS = [
    chk_xcode,
    chk_homebrew,
    chk_zsh,
    chk_python,
    chk_postgres,
    chk_git,
    chk_node,
    chk_shell,
    chk_heroku,
    chk_insomnia,
    chk_vscode,
    chk_env,
]


def chk_ubuntu():
    cmd_match(
        "lsb_release",
        "Distributor ID: Ubuntu",
        "Ubuntu apparently not installed")


def chk_zsh_linux():
    env_match(
        "SHELL",
        "/usr/bin/zsh",
        "Not using correct Zsh")


def chk_python_linux():
    cmd_match(
        "which python3",
        "^/usr/bin/python3$",
        "Python not installed properly")

    cmd_match(
        "which ipython3",
        "^/usr/bin/ipython3$",
        "IPython not installed properly")


def chk_postgres_linux():
    cmd_match(
        "which psql",
        "^/usr/bin/psql$",
        "PostgreSQL not installed correctly")

    cmd_match(
        "psql -V",
        r"^psql .* 12",
        "Wrong PostgreSQL version")


def chk_node_linux():
    cmd_match(
        "which npm",
        "^/usr/bin/npm$",
        "NPM not installed properly")

    cmd_match(
        "node -v",
        "^v18.",
        "Wrong node version")

    cmd_match(
        "nodemon -v",
        "^2",
        "Nodemon not properly installed")


def chk_shell_linux():
    cmd_match(
        "which tree",
        "^/usr/bin/tree$",
        "Tree not installed properly")


def chk_heroku_linux():
    cmd_match(
        "which heroku",
        "^/usr/bin/heroku$",
        "Heroku not installed")


LINUX = [
    chk_ubuntu,
    chk_zsh_linux,
    chk_python_linux,
    chk_postgres_linux,
    chk_git,
    chk_node_linux,
    chk_shell_linux,
    chk_heroku_linux,
    chk_env,
]

# === HERE BE DRAGONS --- SHOULDN'T NEED TO CHANGE THIS STUFF

verbose = False
ok = False


def err(msg, also=""):
    global ok
    print(f"*** {msg}: {also}")
    ok = False


def regex_match(pattern, string):
    result = re.search(pattern, string)
    if verbose:
        print("%s %s ~ %s" % (
            "match" if result else "nomatch",
            pattern,
            string,
        ))
    return result


def cmd_match(cmd, pattern, fail):
    try:
        rez = (subprocess
               .check_output(cmd, shell=True)
               .strip()
               .decode('utf8'))
    except subprocess.CalledProcessError as e:
        if verbose:
            print("  cmderr = %s" % e)
        err(fail, e)
    else:
        if not regex_match(pattern, rez):
            err(fail, rez)


def env_match(envname, pattern, fail):
    val = os.environ.get(envname, "<unset>")
    if not regex_match(pattern, val):
        err(fail, val)


def file_match(path, pattern, fail):
    try:
        with open(path) as f:
            contents = f.read()
            if not regex_match(pattern, contents):
                err(fail, contents[:20])
    except Exception as e:
        if verbose:
            print("  fileerr = %s" % e)
        err(fail, e)


def main():
    global verbose

    verbose = len(sys.argv) > 1 and sys.argv[1] == "-v"

    # for chk in MACOS:
    for chk in LINUX:
        chk()

    if not ok:
        print("""
*** YOU HAVE ERRORS:
    Check installation instructions carefully and follow every step.
    Need help? Run again as '/usr/bin/python %s -v' 
    and submit that output. 
""" % sys.argv[0])
        sys.exit(1)

    print("""
*** EVERY CHECK SUCCESSFUL:
    Congratulations! Please send us the following line:
""")

    # signature
    username = os.environ["USER"]
    sig = (subprocess
           .check_output("echo '%s' | shasum" % username, shell=True)
           .strip()
           .decode('utf8'))
    print("  %s = %s\n" % (username, sig))


if __name__ == "__main__":
    main()
