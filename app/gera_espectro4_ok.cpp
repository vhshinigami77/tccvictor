#include "nilton_basics_ok.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char **argv)
{
    string nome_saida;
    nome_saida = "espectro_";
    nome_saida += argv[1];
    nome_saida += ".txt";

    ofstream saida;
    saida.open (nome_saida.c_str());

    ifstream entrada;
    openIfstream (entrada, argv[2]);

    int total = int(round(2200*atof(argv[3])));//132096;//1111;
    string linha;
    double t[total];
    double y[total];
    double dt;
    int i;

    //geral do SoX
    getline (entrada, linha);
    getline (entrada, linha);
    //

    // double aux;//provisorio

    for (i = 0; i < total; i++)
    {
        // entrada >> t[i] >> y[i] >> aux;
            entrada >> t[i] >> y[i];
            // cout << scientific << t[i] << " " << y[i] << endl;
    }
    // cout << "ok\n";
    // exit (0);
    entrada.close();

    // double f1 = 16.35e0;//261.63e0;
    // double f2 = 1046.5e0;//523.25e0;
    // double df = pow (2e0,1e0/12e0);
    double f1 = 16e0;//261.63e0;
    double f2 = 1048e0;//523.25e0;
    double df = 2e0;//pow (2e0,1e0/12e0);
    int totalf = round ((f2-f1)/df) + 1;

    cout << "df = " << df << endl;
    cout << "totalf = " << totalf << endl;

    double real;
    double imag;
    double magnitude [totalf];

    dt = t[1] - t[0];

    double f;
    int j;
    // double t;
    double maior = 0e0;
    double fmaior;

    for (j = 0; j < totalf; j++)
    {
        real = 0e0;
        imag = 0e0;

        f = f1 + j*df;

        for (i = 0; i < total-1; i++)
        {
            real += y[i]*cos(2e0*pi*f*t[i]);
            imag += -y[i]*sin(2e0*pi*f*t[i]);
        }
        real *= dt;
        imag *= dt;

        // cout << scientific << j << " " << real << " " << imag << endl;

        magnitude [j] = sqrt (real*real + imag*imag);
        if (magnitude [j] > maior)
        {
            fmaior = f;
            maior = magnitude[j];
        }
    }

    for (j = 0; j < totalf; j++)
        saida << f1+j*df << " " << magnitude[j] << endl;

    saida.close();

    cout << fmaior << " Hz\n";



    nome_saida = "resultado_";
    nome_saida += argv[1];
    nome_saida += ".txt";
    saida.open (nome_saida.c_str());
    saida << fmaior << endl << maior << endl;
    saida.close();

    return 0;
}
