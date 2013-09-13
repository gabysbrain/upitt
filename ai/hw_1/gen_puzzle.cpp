#include<stdlib.h>
#include<math.h>
#include<stdio.h>

/***********************************************************************

This code generates  solvable random instances of the  8 puzzle problem
It starts from  a  goal state  hardcoded in 'puzzle' array
and  zeroloc variable  (location  of  0   tile),  then simulates  a
(pseudo) random  walk. Every 'steps' random moves  (steps is hardcoded
to 5) the program generates a problem instance in row major form.

The  instance is  solvable since   reversing the  random moves  in
sequence will  bring us back to the goal state.

Parameters:  #instances requested  and integer  seed for  random number
generation  

Compilation instructions  on elements.cs.pitt.edu:  
g++ -g -lm -opuzzle puzzle.c

Example:
 puzzle 100 3167 > out

*************************************************************************/


int puzzle[] = {1,2,3,4,5,6,7,8,0};
int zeroloc = 8; //important to set the zero location correctly!


int main(int argc, char* argv[]){

  if(argc != 3){
    printf("Usage: puzzle <#instances> <seed>\n");
    exit(1);
  }

  int instances = atoi(argv[1]);
  int seed = atoi(argv[2]);
  srand(seed);
  
  for (int j = 0; j < instances;  j++){  
  

  //Now perturb the solution
  int steps = 5; //(int)rint(rand()*1.0/RAND_MAX * 10);
  
  for (int i = 0;  i < steps; i++){
    bool illegal = true;
    while(illegal){
      int op =  (int) rint (rand() * 1.0 /RAND_MAX * 4);
    switch (op){
      case 1: {
      if ((zeroloc - 1) >= 0 && (zeroloc % 3) > 1){
	int buf = puzzle[zeroloc - 1];
	puzzle[zeroloc-1] = puzzle[zeroloc];
	puzzle[zeroloc] = buf;
	zeroloc -= 1;
	illegal = false;
	break;
      }
    }
    case 2: {
      if(((zeroloc + 1) % 3) > zeroloc){
	int buf = puzzle[zeroloc + 1];
	puzzle[zeroloc + 1] = puzzle[zeroloc];
	puzzle[zeroloc] = buf;
	zeroloc += 1;
	illegal = false;
	break;
      }
    }
    case 3: {
      if((zeroloc -3) > 0){
	int buf = puzzle[zeroloc - 3];
	puzzle[zeroloc - 3] = puzzle[zeroloc];
	puzzle[zeroloc] = buf;
	zeroloc -=3;
	illegal = false;
	break;
      }
    }
    case 4: {
      if((zeroloc + 3) < 9){
	int buf = puzzle[zeroloc + 3];
	puzzle[zeroloc + 3] = puzzle[zeroloc];
	puzzle[zeroloc] = buf;
	zeroloc +=3;
	illegal = false;
	break;
      }         
    }
    }
    }
  }
  for (int i = 0; i<9; i++){
    printf("%d ", puzzle[i]);
  }
    //  if((i+1) % 3 == 0)
    //  printf("\n");    
    //else printf(" ");
    printf("\n");  
  }
}
