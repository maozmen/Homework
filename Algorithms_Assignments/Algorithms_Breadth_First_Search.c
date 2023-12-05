#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

enum {GET = 0, INC, FALSE = 0, TRUE};

#define END 0


int getmatrixsize(FILE *);
int **getmatrix(FILE *, int);
void printmatrix(int **, int);
struct ver *make_vertex(int);
void link_vertex(struct ver *, int);
struct ver *make_vertex_list(int **, int);
void print_vertex_list(struct ver *, int);
void free_vertex_list(struct ver *, int);
int queue_head(int);
int queue_tail(int);
void enqueue(int *, int);
int dequeue(int *);
int *bfs_solve(struct ver *, int, int);
int *bfs_shortest(int *, int, int);
void print_path(int *, int, int);

struct ver{
	int label;
	struct ver *next;
};

int main() {
	
	FILE *f;
	
	f = fopen("Matrix.txt", "r");
	
	int size = getmatrixsize(f);
    int **matrix = getmatrix(f, size);
    fclose(f);
    
    printmatrix(matrix, size);
    
    struct ver *vertex_list;
    vertex_list = make_vertex_list(matrix, size);
    free(matrix);
    print_vertex_list(vertex_list, size);
    
    int start = size - 1;
    int *bfs_solved = bfs_solve(vertex_list, 
	                            size, start);
    
    
    
    int *bfs_path = bfs_shortest(bfs_solved,
	                             start, END);
	                             
	print_path(bfs_path, start, END);
	
	
	free(bfs_solved);
	free(bfs_path);
	free_vertex_list(vertex_list, size);
	
	return 0;
}

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
                
            while(!isblank(c = fgetc(f)) &&
			      c != '\n' && c != EOF){
			    
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

struct ver *make_vertex(int label){
	struct ver *v = (struct ver *)
	                 malloc(sizeof(struct ver));
	v->label = label;
	v->next = NULL;
	return v;
}

void link_vertex(struct ver *v, int label) {
    while(v->next != NULL)
        v = v->next;
    v->next = make_vertex(label);    
}

struct ver *make_vertex_list(int **matrix, int size) {
	struct ver *v_list = (struct ver *)
	                      malloc(sizeof(struct ver) * size);
	
	for (int i = 0; i < size; i++) {
		(v_list + i)->label = i;
		(v_list + i)->next = NULL;
	}
	
	int n;
	
	for (int i = 0; i < size; i++) 
		for (int j = 0; j < size; j++) 
			if (( n = *(*(matrix + i) + j)) != 0){
			    link_vertex(v_list + i, j);
		    }
		
	return v_list;
}

void print_vertex_list(struct ver *v_list, int size) {
	struct ver *v;
	for (int i = 0; i < size; i++) {
		printf("[%d]", i);
        v = v_list + i;
	    while ((v = v->next) != NULL) {
		    printf(" --> [%d]", v->label);
		}

		putchar('\n');	 
	}
	putchar('\n');
}

void free_vertex_list(struct ver *v_list, int size) {
	struct ver *current, *next;
	for(int i = 0; i < size; i++) {
		current = (v_list + i)->next;
		if(current == NULL)
		    continue;
		
		while((next = current->next) != NULL){
			free(current);
			current = next;
		}
		free(current);
	}
	free(v_list);
}

int queue_head(int offset) {
	static int head = -1;
	
	return head += offset;
}

int queue_tail(int offset) {
	static int tail = -1;
	
	return tail += offset;
}

void enqueue(int *queue, int label) {
    *(queue + queue_tail(INC)) = label;	
}

int dequeue(int *queue) {
	if (queue_head(GET) < queue_tail(GET))
	    return *(queue + queue_head(INC));
	else
	    return -1;    
}

int *bfs_solve(struct ver *vertex_list, int size, int start) {
	struct ver *v;
	int center_label, peripheral_label;
	
	int reached[size];
	int *prev_vertex = (int *)malloc(sizeof(int) * size);
	int queue[size];
	
	for (int i = 0; i < size; i++) 
		reached[i] = FALSE;
	
	for(int i = 0; i < size; i++) {
		prev_vertex[i] = -1;
	}
	
	reached[start] = TRUE;
	enqueue(queue, start);
	while((center_label = dequeue(queue)) != -1) {
		reached[center_label] = TRUE;
		v = vertex_list + center_label;
		while((v = v->next) != NULL){
			if(!reached[(peripheral_label = v->label)]){
			    enqueue(queue, peripheral_label);
			    prev_vertex[peripheral_label] = center_label;
		    }
		} 
	}
	
	return prev_vertex;
}

int *bfs_shortest(int *solved, int start, int end){
	int temp, s_size = 1, *s_p, *shortest = NULL;
	//find, end to start shortest path
	s_p = shortest = (int *)malloc(sizeof(int));
	*s_p++ = end;
	do {
		shortest = (int *)realloc(shortest, sizeof(int) * ++s_size);   
		end = shortest[s_size - 1] = solved[end];
	} while(end != start && end != -1);
	
	//reverse the path
	for(int i = 0; i < s_size / 2; i++) {
		temp = shortest[i];
		shortest[i] = shortest[s_size - 1 - i];
		shortest[s_size - 1 - i] = temp;
    }
	
	
	//return start to end shortest path
	return shortest;		
}

void print_path(int *path, int start, int end) {
	printf("shortest path from %d to %d\n[%d]",
	       start, end, *path);
	if (*path == -1){
		printf("\n no such path exists\n");
		return;
	}
	while(1) {
		path++;
		printf(" --> [%d]", *path);
		
		if(*path == end) {
			putchar('\n');
			return;
		}
		if(*path == -1) {
			printf("\n no such path exists\n");
			return;
		}
	}
}

