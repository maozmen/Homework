#include <stdio.h>
#include <stdlib.h>

typedef struct n {
	int number;
	struct n *next;
	struct n *prev;
} node;


int main() {
	
	node *head = NULL, *tail = NULL, *temp;
	
	int cond, n;
	while (1) {
		printf("1. Evet\n2. Hayir\nListeye sayi eklemek istiyor musunuz? ");
		scanf("%d", &cond);
		if(cond == 2)
		    break;
		else if(cond != 1)
		    continue;
		printf("Sayi: ");
		scanf("%d", &n);
		
		if(head == NULL) {
			tail = head = (node *)malloc(sizeof(node));
			head->next = NULL;
			head->prev = NULL;
			head->number = n;
		}
		else {
			tail->next = (node *)malloc(sizeof(node));
			tail->next->prev = tail;
			tail = tail->next;
			tail->next = NULL;
			tail->number = n;	
		}	
	}
	
	temp = head;
	printf("\nListe:\n");
	while(temp != NULL) {
		printf("Onceki adres: %6x, adres: %6x, Sayi:%4d, Sonraki adres: %6x\n",
		       temp->prev, temp, temp->number, temp->next);
		temp = temp->next;       
	}
	putchar('\n');
	
	return 0;
}

