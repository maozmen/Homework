#include <stdio.h>
#include <stdlib.h>

typedef struct nodes{
	int number;
	struct nodes *next;
}node;

int main() {
	node *stack_top = NULL, *queue_head = NULL, *queue_tail = NULL;
	node *new_node, *temp_node;
	int n, choice;
	
	printf("Stack'a sayi eklemek icin 1, Queue'ya sayi eklemek icin 2 girin: ");
	scanf("%d", &choice);
	while(choice == 1 || choice == 2) {
		printf("Sayi: ");
		scanf("%d", &n);
		if (choice == 1) {
			new_node = (node *)malloc(sizeof(node));
			new_node->number = n;
			new_node->next = stack_top;
			stack_top = new_node;	
		}
		else {
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
		printf("Stack'a sayi eklemek icin 1, Queue'ya sayi eklemek icin 2 girin: ");
	    scanf("%d", &choice);	
	}
	
	printf("\n\nStack icindekiler:\n");
	temp_node = stack_top;
	while(temp_node != NULL) {
		printf("Adres: %x, sayi:%4d, sonraki adres: %x\n",
		       temp_node, temp_node->number, temp_node->next);
	    temp_node = temp_node->next;
	}
	
	printf("\nQueue icindekiler:\n");
	temp_node = queue_head;
	while(temp_node != NULL) {
		printf("Adres: %x, sayi:%4d, sonraki adres: %x\n",
		       temp_node, temp_node->number, temp_node->next);
	    temp_node = temp_node->next;
	}
	
	return 0;
}