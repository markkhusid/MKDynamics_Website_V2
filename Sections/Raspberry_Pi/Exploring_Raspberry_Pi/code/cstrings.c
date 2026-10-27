#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    char a[20] = "hello ";
    char b[] = {'w', 'o', 'r', 'l', 'd', '!', '\0'};        // the \0 is important
    
    a[0] = 'H';                                             // set the first character to be H
    char *c = strcat(a, b);                                 // join / concatenate a and b
    
    printf("The string c is: %s\n", c);
    printf("The length of c is: %d\n", strlen(c));          // call string length
    
    // find and replace the w with a W
    char *p = strchr(c, 'w');                               // returns a pointer to first 'w' char
    *p = 'W';
    printf("The string c is now: %s\n", c);
    
    if (strcmp("cat", "dog") <= 0) {                        // ==0 would be equal
        printf("cat comes before dog (lexiographically)\n");
    }
    
    // insert "to the" into middle of "Hello World!" string - very messy!
    char *d = " to the";
    char *cd = malloc(strlen(c) + strlen(d));
    memcpy(cd, c, 5);
    memcpy(cd+5, d, strlen(d));
    memcpy(cd+5+strlen(d), c+5, 6);
    printf("The cd string is: %s\n", cd);
    
    // tokenize cd string using spaces
    p = strtok(cd, " ");
    while (p != NULL) {
        printf("Token: %s\n", p);
        p = strtok(NULL, " ");
    }
    return 0;
}
