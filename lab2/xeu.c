#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
 char *line = NULL;
 size_t linecapp = 0;
 getline(&line, &linecapp, stdin);
 return 0;
}
