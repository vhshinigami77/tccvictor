#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main()
{
    FILE *entrada = fopen(argv[1], "r");
    if (!entrada) {
        fprintf(stderr, "Erro: não foi possível abrir resultado_saida.txt\n");
        return 1;
    }

    double fn, amplitude;
    double limiar = 2e-3;

    if (fscanf(entrada, "%le %le", &fn, &amplitude) != 2) {
        fprintf(stderr, "Erro: formato inesperado em resultado_saida.txt\n");
        fclose(entrada);
        return 1;
    }
    fclose(entrada);

    FILE *saida = fopen("nota.txt", "w");
    if (!saida) {
        fprintf(stderr, "Erro: não foi possível criar nota.txt\n");
        return 1;
    }

    if (amplitude < limiar) {
        fprintf(saida, "PAUSA");
        fclose(saida);
        printf("PAUSA...\n");
        return 0;
    }

    const char* notas[12] = {
        "C", "C#", "D", "D#", "E", "F", "F#",
        "G", "G#", "A", "A#", "B"
    };

    double n = 12 * log(fn / 440.0) / log(2);
    int semitones = round(n + 9);
    int q = semitones / 12;
    int r = semitones % 12;

    printf("%s%d\n", notas[r], 4 + q);
    fprintf(saida, "%s%d", notas[r], 4 + q);
    fclose(saida);

    return 0;
}
