#ifndef NILTON_BASICS_H
#define NILTON_BASICS_H

#include <iostream>
#include <cmath>
#include <fstream>
#include <cstdlib>
#include <sstream>

using std::cin;
using std::cout;
using std::endl;
using std::string;
using std::ostringstream;

using std::ifstream;
using std::ofstream;
using std::scientific;
using std::getline;

int s2Int (string s);
double s2Double (string s);
string int2Str (int i);
string d2Str (double i);

string nameOk (string s, string formato);
string nameLabel (string s, string formato, string label);
void ignoreLines (ifstream &entrada, int numero);
void copyLines (ifstream &entrada, ofstream &saida, int numero);
string saveLine (ifstream &entrada, int numero);
void ignoreStrings (ifstream &entrada, int numero);
void fixLs (string nome, string formato);
double valorMaximo (string nome, string tipo);
double valorMaximoAbs (string nome, string tipo);
double valorMinimo (string nome, string tipo);
void salvaIntervalos (string lista);
void imprimeArray (double *vetor, int size);
void inicializaArray (double *vetor, int size, double valor);
void openIfstream (ifstream &entrada, string nome);
string ajustaSubstring (string sub, string caractere);
string leAntesCaractere (string linha, string caractere, int maximo, int vez); //se vez > maximo: captura o restante da string
int totalLines (ifstream &entrada, int caso);//caso == 1: despreza linhas vazias
int totalCaracteres (string s, string key);
string alteraCaractere (string s, string caractere, string novo);

void reload (ifstream &file, string nome);
void normaliza (string nome, double valor);

#define pi 3.141592653589793

#endif // NILTON_BASICS_H
