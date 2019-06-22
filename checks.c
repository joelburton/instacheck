/** Edit this function to change the tests that this runs. */

#include "instacheck.h"

/** Test runner:
 *
 * Useful things you can call inside of here:
 *
 *   err(str)  - to print string like an error
 *   warn(str) - to print string like a warning
 *
 *   cmdMatch(shellCommand, regex) - return true if command output matches regex
 *   envMatch(envName, regex) - return true if $envName matches regex
 *
 * This function should return true/false for good-installation-or-not.
 *
 */

bool doChecks() {
    bool ok = true;

    // xcode

    if (!cmdMatch("xcode-select -p", "^/Applications/Xcode.app/Contents/Developer")) {
        err("Xcode not installed");
        ok = false;
    }

    // homebrew itself

    if (!cmdMatch("which brew", "^/usr/local/bin/brew$")) {
        err("Homebrew not installed properly");
        ok = false;
    }
    
    // python version & not in a venv

    if (!cmdMatch("which python3", "^/usr/local/bin/python3$")) {
        err("Python not installed properly");
        ok = false;
    }

    if (!cmdMatch("which ipython", "^/usr/local/bin/ipython$")) {
        err("IPython not installed properly");
        ok = false;
    }

    // node + npm

    if (!cmdMatch("which npm", "^/usr/local/bin/npm$")) {
        err("NPM not installed properly");
        ok = false;
    }

    if (!cmdMatch("node -v", "^v10.")) {
        err("Wrong node version");
        ok = false;
    }

    // postgresql

    if (!cmdMatch("which psql", "^/usr/local/bin/psql$")) {
        err("PostgreSQL not installed correctly");
        ok = false;
    }

    if (!cmdMatch("psql -V", "^psql .* 11\\.")) {
        err("Wrong PostgreSQL version");
        ok = false;
    }

    // vscode

    if (!cmdMatch("which code", "^/usr/local/bin/code$")) {
        err("VSCode not installed or 'code' command not set up");
        ok = false;
    }

    // heroku

    if (!cmdMatch("which heroku", "^/usr/local/bin/heroku$")) {
        err("Heroku not installed");
        ok = false;
    }

    // tree

    if (!cmdMatch("which tree", "^/usr/local/bin/tree$")) {
        err("Tree not installed properly");
        ok = false;
    }

    // bash

    if (!envMatch("SHELL", "^/opt/local/bin/bash$")) {
        err("Not using bash as your shell");
        ok = false;
    }

    // our bash profile stuff

    if (!envMatch("FLASK_ENV", "^development$")) {
        err("Wrong or missing $FLASK_ENV; did you get our bash setup?");
        ok = false;
    }

    // git setup


    if (!cmdMatch("grep gitignore_global ~/.gitconfig", "gitignore_global"))
        err(".gitconfig is not set up with our commands");

    if (!cmdMatch("grep venv ~/.gitignore_global", "venv"))
        err(".gitignore_global does not contain our contents");

    return ok;
}
