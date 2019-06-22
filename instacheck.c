/** Setup checking program.
 *
 * You SHOULD NOT NEED to edit this file to add/edit tests.
 * Instead, edit `checks.c`.
 *
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <regex.h>

bool doChecks();
unsigned char *SHA1(const unsigned char *d, size_t n, unsigned char *md);


// set with -v switch on cmdline
bool verbose = false;



/** Does regex pattern match string? 
 *
 * Returns true/false
 *
 */


bool regexMatch(char *pattern, char *string) {
    int reti;
    char msgbuf[100];
    regex_t regex;

    // compile regex & handle compilation errs
    
    reti = regcomp(&regex, pattern, REG_EXTENDED);
    if (reti) {
        fprintf(stderr, "\n\n*** FATAL: could not compile regex: %s\n", pattern);
        exit(1);
    }

    // compare regex to pattern

    reti = regexec(&regex, string, 0, NULL, 0);
    if (!reti) {
        if (verbose) printf("match \"%s\" ~ \"%s\"\n", pattern, string);
    }
    else if (reti == REG_NOMATCH) {
        if (verbose) printf("nomatch \"%s\" ~ \"%s\"\n", pattern, string);
    }
    else {
        regerror(reti, &regex, msgbuf, sizeof(msgbuf));
        fprintf(stderr, "\n\n*** FATAL: Regex match failed: %s\n", msgbuf);
        exit(1);
    }

    regfree(&regex);
    return (!reti);
}

/** Run shell command and see if output matches regex
 *
 * Returns true/false
 *
 */

bool cmdMatch(char *cmd, char *pattern) {
    FILE *fp;
    char result[4096];

    // Open the command for reading

    fp = popen(cmd, "r");
    if (fp == NULL) {
        printf("*** ERROR: failed to run command %s\n", cmd);
        return false;
    }

    fgets(result, sizeof(result)-1, fp);
    pclose(fp);
    
    // trim last newline
    result[strlen(result)-1] = '\0';

    if (verbose) printf("Command \"%s\" returned \"%s\":\n  ", cmd, result);

    return regexMatch(pattern, result);
}


/** Compare environmental variable against regex
 *
 * Returns true/false
 *
 */

bool envMatch(char *envName, char *pattern) {
    char *result = getenv(envName);

    if (verbose) printf("Env $%s is \"%s\":\n  ", envName, result);

    return result != NULL && regexMatch(pattern, result);
}


/** Print error message & set global state to error-happened. */

void err(char *msg) {
    printf("*** ERROR: %s\n\n", msg);
}


/** Main: run checks, report success or failure. */

int main(int argc, char **argv) {

    if (argc == 2 && strcmp(argv[1], "-v") == 0) verbose = true;

    bool ok = doChecks();

    if (!ok) {
        printf("\n*** YOU HAVE ERRORS:\n");
        printf(
            "  Check installation instructions carefully & follow every step.\n"
            "  Need help? Run again as `./check -v' and submit that output.\n");
        return EXIT_FAILURE;
    }

    printf("\n*** EVERY CHECK SUCCESSFUL:\n");
    printf("  Congratulations! Please send us the following line:\n");

    // create SHA-1 of their name
    const unsigned char *username = (const unsigned char *) getenv("USER");
    const long n = strlen((const char *) username);
    unsigned char *rez = SHA1(username, n, NULL);

    printf("  %s = ", username);
    for(int i = 0; i < 16; i++) printf("%02x", rez[i]);
    printf("\n");

    return EXIT_SUCCESS;
}

