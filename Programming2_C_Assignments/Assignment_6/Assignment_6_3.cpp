#include <stdio.h>
#include <stdlib.h>

typedef struct n {
	int number;
	struct n *next;
	struct n *prev;
} node;


int main() {
	
	node *head = NULL, *temp;
	
	int cond, n;
	while (1) {
		printf("1. Evet\n2. Hayir\nSirali listeye sayi eklemek istiyor musunuz? ");
		scanf("%d", &cond);
		if(cond == 2)
		    break;
	    else if(cond != 1)
	        continue;
		printf("Sayi: ");
		scanf("%d", &n);
		
		if(head == NULL) {
			head = (node *)malloc(sizeof(node));
			head->next = NULL;
			head->prev = NULL;
			head->number = n;
		}
		else {
			temp = head;
			while(temp->next != NULL && temp->number < n) 
			    temp = temp->next;
		    
			if(temp->number >= n) {
				if(temp->prev == NULL) {
					temp->prev = (node *)malloc(sizeof(node));
					head =temp->prev;
					head->prev = NULL;
					head->next = temp;
					head->number = n;
				}
				else {
					temp->prev->next = (node *)malloc(sizeof(node));
					temp->prev->next->prev = temp->prev;
					temp->prev = temp->prev->next;
					temp->prev->next = temp;
					temp->prev->number = n;
				}
			}
			else {
				temp->next = (node *)malloc(sizeof(node));
				temp->next->prev = temp;
				temp->next->next = NULL;
				temp->next->number = n;
			}
		}
    }
	
	temp = head;
	printf("\nSirali liste:\n");
	while(temp != NULL) {
		printf("Onceki adres: %6x, adres: %6x, Sayi:%4d, Sonraki adres: %6x\n",
		       temp->prev, temp, temp->number, temp->next);
		temp = temp->next;       
	}
	putchar('\n');
	
	
    return 0;	
}