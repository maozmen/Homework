#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define COUNT 100
#define FILENAME "sayilar.txt"

int main() {
    FILE *f;
    f = fopen(FILENAME, "w");
    char s[21];
    
    srand(time(NULL));
    
    for (int i = 0; i < COUNT; i++) {
        sprintf(s, "%d", (int) rand() % 1000);
        fprintf(f, "%s ", s);
        if (i % 10 == 9)
            fprintf(f, "\n");
    }
    
    fclose(f);
    
    return 0;
}