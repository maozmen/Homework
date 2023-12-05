#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int getmatrixsize(FILE *);
int **getmatrix(FILE *, int);
void printmatrix(int **, int);
void nodeio(int *, int **, int);
void askprintnodeio(int *);
void printedgecount(int *, int);
void printedgetotalcost(int **, int);
void askprintadjacent(int **, int);
void iscomplete(int **, int);
void isdirected(int **, int);

int main()
{
    FILE *f;
    int size;
    int **matrix;

    f = fopen("Odev_1.txt", "r");
    size = getmatrixsize(f);
    matrix = getmatrix(f, size);
    fclose(f);
    
    printmatrix(matrix, size);
    
	int nodeioarr[size * 2];
    nodeio(nodeioarr, matrix, size);
    askprintnodeio(nodeioarr);
    
    printedgecount(nodeioarr, size);
    
    printedgetotalcost(matrix, size);
    
    askprintadjacent(matrix, size);
    
    iscomplete(matrix, size);
    
    isdirected(matrix, size);
    
	return 0;    
}

//returns size of the square matrix in the file
//returns file pointer to the start!
int getmatrixsize(FILE *f)
{
    fseek(f, 0L, SEEK_SET);
    int n = 0;
    char c;
    char in = 0;

    while ((c = fgetc(f)) != EOF) {

        if(isdigit(c)) {
            if(!in) {
                n++;
                in = 1;
            }
        } else
            in = 0;
        if (c == '\n' && n != 0)
            break;
    }
    fseek(f, 0L, SEEK_SET);

    return n;
}

int **getmatrix(FILE *f, int size)
{
    int  c, n, *r, *row, **m, **matrix;
    char  p1[11], *p2;
    matrix = (int **) malloc(sizeof(int *) * size);
    m = matrix;

    for (int i = 0; i < size; i++) {
        r = row = (int *) malloc(sizeof(int) * size);

        for (int j = 0; j < size; j++) {
        	p2 = p1;
            while (isblank(c = fgetc(f))) ;
            if(isdigit(c))
                *p2++ = c;
                
            while(!isblank(c = fgetc(f)) && c != '\n' && c != EOF){
			    
                if (isdigit(c))
                    *p2++ = c;
            }
			*p2 = '\0';
            n = atoi(p1);
            *r++ = n;

            if((j == size - 1) && isblank(c))
                while(isblank(c = fgetc(f))) ;
        }
        *m++ = row;
    }
    return matrix;
}

void printmatrix(int **matrix, int size)
{
	putchar('\n');
	
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            printf("%3d ", *(*(matrix + i) + j));
        }
        putchar('\n');
    }
    putchar('\n');
}

void nodeio(int *arr, int **matrix, int size) {
	for (int i = 0; i < size * 2; i++)
	    *(arr + i) = 0;
	    
	for (int i = 0; i < size; i++) 
		for (int j = 0; j < size; j++) 
			if (*(*(matrix + i) + j) != 0) {
			    (*(arr + 2 * j))++;      //incoming
			    (*(arr + 2 * i + 1))++;  //outgoing
			}
}

void askprintnodeio(int *arr) {
	int node;
	printf("Giris cikis derecesi hesaplanacak dugum: ");
	scanf("%d", &node);
	printf("\n%d. Dugum icin giris derecesi: %d, cikis derecesi: %d\n\n",
	       node, arr[2 * node], arr[2 * node + 1]);
}

void printedgecount(int *arr, int size) {
	int sum = 0;
	
	for (int i = 0; i < size; i++) 
		sum += *(arr + i * 2);
	
	printf("Graftaki toplam kenar sayisi: %d\n\n", sum);
}

void printedgetotalcost(int **matrix, int size) {
	int sum = 0;
	
	for (int i = 0; i < size; i++) 
		for (int j = 0; j < size; j++) 
			sum += *(*(matrix + i) + j);
		
	printf("Graftaki kenar maliyetleri toplami: %d\n\n", sum);
}

void askprintadjacent(int **matrix, int size) {
	int cost, node, first = 1;
	
	printf("Komsuluklari ve komsuluklarinin maliyetleri hesaplanacak dugum: ");
	scanf("%d", &node);
	
	printf("\nGraftaki %d. dugumun komsulari: ", node);
	for (int i = 0; i < size; i++) {
		if((cost = *(*(matrix + node) + i)) != 0){
			if(!first)
			    printf("; ");  
			else
			    first = 0;    
			printf("%d. dugum, maliyet: %d", i, cost);	  
		}
	}
	printf("\n\n");
}

void iscomplete(int **matrix, int size) {
	int complete = 1;
	for(int i = 0; i < size; i++){
	    if (!complete)
	        break;
		for(int j = 0; j < size; j++)
		    if(i == j){
		    	complete = *(*(matrix + i) + j) == 0 ? 1 : 0;
		    	continue;
			} 
		    else if(*(*(matrix + i) + j) == 0){
		        complete = 0;
	            break;
        }
    }
    
    complete ? printf("Graf tam bagli graftir.") :
    	printf("Graf tam bagli graf degildir.");
    	
    printf("\n\n");	
} 

void isdirected(int **matrix, int size) {
	int directed = 0;
	
	for (int i = 0; i < size; i++) {
		if (directed)
		    break;
		for (int j = i + 1; j < size; j++) 
			if(*(*(matrix + i) + j) != *(*(matrix + j) + i)){
			    directed = 1;
			    break;
		    }
	}
	
	directed ? printf("Graf yonludur.") : printf("Graf yonlu degildir.");
	printf("\n\n");
}