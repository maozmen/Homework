#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 20

void swap(int *, int *);
void selection_sort(int *, int);

int main() {
	int *arr = (int *)malloc(sizeof(int) * SIZE);
	
	srand(time(NULL));
	for (int i = 0; i < SIZE; i++) {
		*(arr + i) = rand() % 99 + 1;
	}
	
	selection_sort(arr, SIZE);
	
	for (int i = 0; i < SIZE; i++) {
		printf("arr[%2d]: %2d\n", i, *(arr + i));
	}
	
	return 0;
}

void swap(int *x, int *y) {
	int temp;
	temp = *x;
	*x = *y;
	*y = temp;
}

void selection_sort(int *arr, int size) {
	int *max;
	
	for(int i = 0; i < size - 1; i++) {
	    max = arr + i;	
		for(int j = i + 1; j < size; j++) {
			if (*max < *(arr + j))
			    max = arr + j;
		}
		swap(arr + i, max);
	} 
}