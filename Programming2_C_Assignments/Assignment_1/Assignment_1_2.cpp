#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define FILENAME1 "sayilar.txt"
#define FILENAME2 "sayilar2.txt"
#define COUNT 100

int isprime(int);
void fgetns(char *, FILE *);

int main() {
    FILE *f1, *f2;
    char s[23];
    f1 = fopen(FILENAME1, "r");
    int n;
    int primecount = 0;    
    f2 = fopen(FILENAME2, "w");
    for (int i = 0; i < COUNT; i++) {
        fgetns(s, f1);
        if(isprime(n = atoi(s))) {
            sprintf(s, "%d", n);
            fprintf(f2, "%s ", s);
			if (++primecount % 10 == 9)
			    fprintf(f2, "\n");   
        }
	}
    fclose(f2);
    
    return 0;
}

int isprime(int n) {
    int i = 2;
    
    while(1) {
        if (n % i == 0)
            return 0;
        if (i * i > n)
            return 1;
        i++;        
    }
}

void fgetns(char *s, FILE *f) {
	char c;
	int in = 0;
	int end = 0;
	
	while ((c = fgetc(f)) != EOF) {
		if (isdigit(c))
		    if (!end) {
			    *s++ = c;
		        in = 1;
		    }
		    else {
		    	break;
			}
		else if (in) {
			in = 0;
			end = 1;
		}	
	}
	*s = '\0';
	
	fseek(f, ftell(f) - 1, SEEK_SET);	
}