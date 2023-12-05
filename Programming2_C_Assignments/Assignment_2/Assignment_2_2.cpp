#include <stdio.h>

int sumtill (int);

int main() {
	int x = 10000;
	
	printf("(0)-(%d) arasindaki pozitif tam sayilarin toplami: %d\n", x, sumtill(x));

    return 0;
}

int sumtill(int x) {
	if (x <= 0)
	    return 0;
    
	return x + sumtill(x - 1); 
}