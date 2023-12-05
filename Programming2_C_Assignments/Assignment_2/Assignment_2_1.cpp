#include <stdio.h>
#include <math.h>

int obeb(int, int, int);

int main() {
	int x = 34848;
	int y = 23936;
	
	printf("obeb(%d, %d) = %d\n", x, y, obeb(x, y, 2));
	
	return 0;
}

int obeb(int x, int y, int b) {
	int min =  x < y ? x : y;
	int max = x > y ? x : y;
	
	if (b < 2)
	    b = 2;
	
	for(int i = b; i < min; i++) {
		if (min % i == 0) 
		    if (max % i == 0)
		        return i * obeb(max / i, min / i, i);
		    else if (max % (min / i) == 0)
		        return (min / i) * obeb((max * i) / min, i, i);
        
		if (i * i >= min)
		    break;    
	}
	
	return max % min == 0 ? min : 1;
}