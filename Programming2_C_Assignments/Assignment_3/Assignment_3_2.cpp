#include <stdio.h>
#include <stdlib.h>
#include <time.h>

unsigned int makezero(unsigned int, int);
unsigned int makeone(unsigned int, int);
unsigned int isone(unsigned int, int);

int main() {
	FILE *f1, *f2;
	
	f1 = fopen("sayilar0.txt", "w");
	f2 = fopen("sayilar1.txt", "w");
	
	srand(time(NULL));
	
	int n;
	for(int i = 0; i < 100; i++) {
		if (isone(n = rand() % 99 + 1, 5))
		    fprintf(f2, "%u ", makezero((unsigned int) n, 3));
		else 
		    fprintf(f1, "%u ", makeone((unsigned int) n, 4));	  
    }
	fclose(f1);
	fclose(f2);
	
	return 0;
}



unsigned int makezero(unsigned int n, int index) {
	return n & ~(1 << index);
}

unsigned int makeone(unsigned int n, int index) {
	return n | 1 << index;
}

unsigned int isone(unsigned int n, int index) {
	return n & 1 << index;
	
}


