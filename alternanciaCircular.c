#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define clear() printf("\033[H\033[J")

typedef struct processo {
    int PID;
    int criacao;
    int fim;
    int tempoRestante;
    int UID;
} Processo;

void alternanciaCircular(int cpuFraction){
    // Posição 11 = PID, 13 = Tempo Execução, 17 = UID
    FILE *fptr;
    fptr = fopen("input.txt", "r");
    Processo vetProcessos[10000];

    size_t read;
    size_t len=0;
    char *line;
    int i=0;
    int cpuTime = 0, totalCPUtimeleft = 0;
    read = getline(&line, &len, fptr);

    while ((read = getline(&line, &len, fptr)) != -1){
        vetProcessos[i].PID = line[11] - '0';
        vetProcessos[i].tempoRestante = line[13] - '0';
        vetProcessos[i].UID = line[17] - '0';
        vetProcessos[i].criacao = cpuTime;
        totalCPUtimeleft += line[13] - '0';
        i++;
    }
    
    int j;

    // enquanto vetProcessos não está vazio
    while(totalCPUtimeleft != 0){
        for (j=0;j<i;j++){
            printf("Processo %d executando...\n", j);
            printf("Tempo restante: %d\n", vetProcessos[j].tempoRestante);
            if (cpuFraction <= vetProcessos[j].tempoRestante){
                cpuTime += cpuFraction;
                vetProcessos[j].tempoRestante -= cpuFraction;
                totalCPUtimeleft -= cpuFraction;
            } else if (cpuFraction > vetProcessos[j].tempoRestante){
                cpuTime += vetProcessos[j].tempoRestante;
                totalCPUtimeleft -= vetProcessos[j].tempoRestante;
                vetProcessos[j].tempoRestante = 0;
                vetProcessos[j].fim = cpuTime;
            }
            sleep(0.1); // ajustar esse valor para ver mais claramente no terminal
            clear();
            
        }
    }
    printf("Todos os processos terminaram, tempo final de CPU: %d\n", cpuTime);



}