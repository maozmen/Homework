#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NCOUNT 100

int isone(unsigned int, int);

int main() {
	FILE *f = fopen("sayi.txt", "w+");
	
	srand(time(NULL));
	for (int i = 0; i < NCOUNT; i++)
	    fprintf(f, "%u ", (unsigned int)(rand() % 99 + 1));
	
	unsigned int n, *arr, size = 0;
	rewind(f);
	for (int i = 0; i < NCOUNT; i++){
	    fscanf(f, "%u", &n);
	    if(!isone(n, 5)){
	    	if (!size++){
	    		arr = (unsigned int *)malloc(sizeof(unsigned int));
	    		*(arr + size - 1) = n;
			}
			else {
				arr = (unsigned int *)realloc(arr, sizeof(unsigned int) * size);
				*(arr + size - 1) = n;
			}
		}
	}
	fclose(f);
	
	for (int i = 0; i < size; i++)
	    printf("arr[%2d]: %u\n", i, *(arr + i)); 
    
	free(arr);    
	
	return 0;
}

int isone(unsigned int n, int pos) {
	return n & 1 << pos;
}