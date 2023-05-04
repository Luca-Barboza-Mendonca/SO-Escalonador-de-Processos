#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "alternanciaCircular.c"

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
    int cpuFrac = line[20] - '0';
    fclose(fptr);

    if (metodoDeEscalonamento == 'a') {
        alternanciaCircular(cpuFrac);
    }

}

int main() {
    readf();
}