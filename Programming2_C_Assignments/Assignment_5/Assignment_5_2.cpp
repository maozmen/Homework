#include <stdio.h>
#include <stdlib.h>

void add(int, int);
void find_remove(int, int);
void find_display(int, int);
void display_all(int);

typedef struct nodes{
	int number;
	struct nodes *next;
}node;

node *stack_top = NULL, *queue_head = NULL, *queue_tail = NULL;

int main() {
	int choice_structure, choice_function, n;
	while(1) {
		printf("1. Stack\n2. Queue\nKullanilacak veri yapisini secin: ");
		scanf("%d", &choice_structure);
		if(choice_structure < 1 || choice_structure > 2){
			printf("\n1. Evet\n2. Hayir\nProgram kapansin mi? ");
			scanf("%d",&choice_structure);
			putchar('\n');
			if(choice_structure == 1)
			    break;
			else
			    continue;
		}
		printf("\n1. Ekle\n2. Bul ve Sil\n3. Bul ve Goster\n");
		printf("4. Tumunu Listele\nYapilacak islemi secin: ");
		scanf("%d", &choice_function);
		if(choice_function < 1 || choice_function > 4){
		    printf("\n1. Evet\n2. Hayir\nProgram kapansin mi? ");
			scanf("%d",&choice_function);
			putchar('n');
			if(choice_function == 1)
			    break;
			else
			    continue;
	    }
		switch(choice_function) {
			case 1:
				printf("Eklenecek sayi: ");
				scanf("%d", &n);
				add(choice_structure, n);
				break;
			case 2:
				printf("Aranacak sayi: ");
				scanf("%d", &n);
				find_remove(choice_structure, n);
				break;				
			case 3:
				printf("Aranacak sayi: ");
				scanf("%d", &n);
				find_display(choice_structure, n);
				break;
			case 4:
			    display_all(choice_structure);
				break;	
		    default:
		    	break;
		}
		putchar('\n');
	}
	
	return 0;
}

void add(int structure, int n) {
	node *new_node;
	if(structure == 1) {
		new_node = (node *)malloc(sizeof(node));
		new_node->number = n;
		new_node->next = stack_top;
		stack_top = new_node;	
	}
	else if(structure == 2){
		new_node = (node *)malloc(sizeof(node));
		new_node->number = n;
		new_node->next = NULL;
		if(queue_tail == NULL)
			queue_tail = queue_head = new_node;
		else {
			queue_tail->next = new_node;
	        queue_tail = new_node;
		}			
	}
}

void find_remove(int structure, int n) {
	node *temp_node1, *temp_node2;
	if(structure == 1) {
		if(stack_top == NULL)
		    printf("Stack yapisi bos.\n");
		else {
			temp_node1 = stack_top;
			if (temp_node1->number == n) {
				stack_top = temp_node1->next;
				free(temp_node1);
			}
			else {
				while((temp_node2 = temp_node1->next) != NULL){
					if(temp_node2->number == n) {
						temp_node1->next = temp_node2->next;
						free(temp_node2);
						break;
					}
					temp_node1 = temp_node2;
				}
			}	
		}
	}
	else if(structure == 2) {
		if(queue_head == NULL) {
			printf("Queue yapisi bos.\n");
		}
		else {
			temp_node1= queue_head;
			if(temp_node1->number == n) {
				queue_head = temp_node1->next;
				free(temp_node1);
				if(queue_head == NULL)
				    queue_tail = NULL;
			}
			else {
				while((temp_node2 = temp_node1->next) != NULL) {
					if(temp_node2->number == n) {
						temp_node1->next = temp_node2->next;
						free(temp_node2);
						if(temp_node1->next == NULL)
						    queue_tail = temp_node1;
						break;    
					}
					temp_node1 = temp_node2;
				}
			}
		}
	}
}

void find_display(int structure, int n) {
	node *temp_node;
	if(structure == 1) {
		temp_node = stack_top;
		if(temp_node == NULL)
		    printf("Stack yapisi bos.\n");
	    else {
	    	while(temp_node != NULL) {
	    		if(temp_node->number == n){
	    		    printf("Adres: %x, sayi:%4d, sonraki adres: %x\n",
	    		           temp_node, temp_node->number, temp_node->next);
	    		    break;
				}
				temp_node = temp_node->next;
			}
			if(temp_node == NULL)
			    printf("%d sayisi stack'ta yok.\n", n);
		}
	}
	else if(structure == 2) {
		temp_node = queue_head;
		if(temp_node == NULL) 
		    printf("Queue yapisi bos.\n");
	    else {
	    	while(temp_node != NULL) {
	    		if(temp_node->number == n) {
	    			printf("Adres: %x, sayi:%4d, sonraki adres: %x\n",
	    			       temp_node, temp_node->number, temp_node->next);
	    			break;       
				}
				temp_node = temp_node->next;
			}
			if(temp_node == NULL)
			    printf("%d sayisi queue'da yok.\n", n);
		}
	}
}

void display_all(int structure) {
	node *temp_node;
	if(structure == 1) {
		temp_node = stack_top;
		printf("\nStack icindekiler:\n");
		while(temp_node != NULL) {
			printf("Adres: %x, sayi:%4d, sonraki adres: %x\n",
			       temp_node, temp_node->number, temp_node->next);
		    temp_node = temp_node->next;
	    }
	}
	else if(structure == 2) {
		temp_node = queue_head;
		printf("\nQueue icindekiler:\n");
		while(temp_node != NULL) {
			printf("Adres: %x, sayi:%4d, sonraki adres: %x\n",
			       temp_node, temp_node->number, temp_node->next);
		    temp_node = temp_node->next;
		}		
	}
}
