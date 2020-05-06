#include <stdbool.h>

bool regexMatch(char *pattern, char *string);
bool cmdMatch(char *cmd, char *pattern);
bool envMatch(char *envName, char *pattern);
void err(char *msg);

