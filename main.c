#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void readf(){
    FILE *fptr;
    fptr = fopen("input.txt", "r");

    size_t read;
    size_t len=0;
    char *line;
    char metodoDeEscalonamento;
    line = (char *) malloc(100 * sizeof(char));

    if (fptr == NULL){
        printf("Falha ao ler entrada");
    }

    read = getline(&line, &len, fptr);
    // a = alternancia circular
    // l = loteria
    // p = prioridade
    metodoDeEscalonamento = line[0];

    // Token vai guardar a fração de cpu
    char *cpuFrac;

    cpuFrac = strtok(line, "|");
    printf("Token: %c\n", *cpuFrac);
    

}

int main() {
    readf();
}