#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main()
{
    FILE *entrada;
    entrada = fopen ("resultado_saida.txt", "r");
    
    double fn;
    double amplitude;
    double limiar = 2e-3; 
    fscanf (entrada, "%le %le", &fn, &amplitude);
    fclose (entrada);
    
    FILE *saida;
    saida = fopen ("nota.txt", "w");

    //
    if(amplitude < limiar){
        printf("PAUSA...\n");
        exit (0);
    }

    char notas[12][10];
    sprintf (notas[0],"C");
    sprintf (notas[1],"C#");
    sprintf (notas[2],"D");
    sprintf (notas[3],"D#");
    sprintf (notas[4],"E");
    sprintf (notas[5],"F");
    sprintf (notas[6],"F#");
    sprintf (notas[7],"G");
    sprintf (notas[8],"G#");
    sprintf (notas[9],"A");
    sprintf (notas[10],"A#");
    sprintf (notas[11],"B");
    //
    
    double n;
    int r;
    int q;
    
    //
    n = 12*log(fn/440)/log (2);
    q = (int)(round (n+9))/12;
    r = (int)(round (n+9))%12;
    
//    printf ("%lf %d %d\n", n, q, r);
    printf ("%s%d", notas[r],4+q);
    
    
    fprintf (saida, "%s%d", notas[r],4+q);
    fclose (saida);
    printf("\n");

    return 0;
}
