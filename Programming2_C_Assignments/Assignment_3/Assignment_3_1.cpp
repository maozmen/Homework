#include <stdio.h>

unsigned int rotateleft(unsigned int, int);

int main() {
	unsigned int n;
	int count;
	printf("sayiyi ve sayinin kac kez sola rotate shift yapilacagini");
	printf(" arada bir bosluk birakarak girin: ");
	scanf("%u %u", &n, &count);
	
	printf("sonuc: %u\n", rotateleft(n, count));

}


unsigned int rotateleft(unsigned int n, int count){
	while(--count >= 0)
	    if(n & 1 << sizeof(unsigned int) * 8 - 1)
	        n = n << 1 | 1;
        else
            n <<= 1;
    return n;
}