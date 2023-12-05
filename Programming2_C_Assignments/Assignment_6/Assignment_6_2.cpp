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
	
	while(1) {
		printf("1. Evet\n2. Hayir\nListeden sayi silmek istiyor musunuz? ");
		scanf("%d", &cond);
		if(cond == 2)
		    break;
		else if(cond != 1)
		    continue;
		printf("Sayi: ");
		scanf("%d", &n);
		if(head == NULL) {
			printf("Liste bos.\n");
			break;
		}    
		cond = 1;
		temp = head;
		while(temp != NULL) {
			if(temp->number == n){
				printf("Silinecek sayi:%4d, onceki adresi: %6x, adresi: %6x, sonraki adresi: %6x",
				       temp->number, temp->prev, temp, temp->next);
				if(temp->prev == NULL) 
					head = head->next;
				else 
					temp->prev->next = temp->next;
					
				if(temp->next == NULL) 
					tail = tail->prev;
				else 
					temp->next->prev = temp->prev;
				free(temp);
				break;
			}
			temp = temp->next;
		}
		if(cond)
		    printf("Aranan sayi listede yok.\n");
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

