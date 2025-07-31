#include "nilton_basics_ok.h"

int s2Int (string s)
{
    int a = atoi (s.c_str());

    return a;
}


double s2Double (string s)
{
    double a = atof (s.c_str());

    return a;
}

string int2Str (int i)
{
    ostringstream a;
    a << i;

    return a.str();
}

string d2Str (double i)
{
    ostringstream a;
    a << i;

    return a.str();
}

string nameOk (string s, string formato)
{
    ostringstream ss;
    int size = formato.length();
    string sub = s.substr (0, s.length() - (size+1));
    ss << sub << "_ok." << formato;

    return ss.str();
}

string nameLabel (string s, string formato, string label)
{
    ostringstream ss;
    int size = formato.length();
    string sub = s.substr (0, s.length() - (size+1));
    ss << sub << "_" << label << "." << formato;

    return ss.str();
}

void ignoreLines (ifstream &entrada, int numero)
{
    string linha;

    for (int i = 1; i <= numero; i++)
        getline (entrada, linha);
}

void copyLines (ifstream &entrada, ofstream &saida, int numero)
{
    string linha;

    for (int i = 1; i <= numero; i++)
    {
        getline (entrada, linha);
        saida << linha << endl;
    }
}

string saveLine (ifstream &entrada, int numero)
{
    string linha;

    for (int i = 1; i <= numero; i++)
        getline (entrada, linha);
    return linha;
}

void ignoreStrings (ifstream &entrada, int numero)
{
    string linha;

    for (int i = 1; i <= numero; i++)
        entrada >> linha;
}

void fixLs (string nome, string formato)
{
    string name_out = nameOk (nome, formato);

    ifstream entrada;
    ofstream saida;

    entrada.open (nome.c_str());
    saida.open (name_out.c_str());

    string linha;

    int total = -1;

    while (!entrada.eof())
    {
        getline (entrada, linha);
        total++;
    }

    entrada.close();

    entrada.open (nome.c_str());

    for (int i = 1; i <= total; i++)
    {
        ignoreStrings (entrada, 4);
        entrada >> linha;
        saida << linha << endl;
    }
    entrada.close();
    saida.close();
}

double valorMaximo (string nome, string tipo)
{
    double x;
    double y;

    ifstream entrada;
    entrada.open(nome.c_str());

    double xmax;
    double ymax;

    entrada >> x >> y;
    xmax = x;
    ymax = y;

    while (!entrada.eof())
    {
        entrada >> x >> y;
        if (y > ymax)
        {
            xmax = x;
            ymax = y;
        }
    }

    entrada.close();

    if (tipo == "x") return xmax;
    else return ymax;
}

double valorMaximoAbs (string nome, string tipo)
{
    double x;
    double y;

    ifstream entrada;
    entrada.open(nome.c_str());

    double xmax;
    double ymax;

    entrada >> x >> y;
    xmax = x;
    ymax = fabs(y);

    while (!entrada.eof())
    {
        entrada >> x >> y;
        if (fabs(y) > ymax)
        {
            xmax = x;
            ymax = fabs(y);
        }
    }

    entrada.close();

    if (tipo == "x") return xmax;
    else return ymax;
}

double valorMinimo (string nome, string tipo)
{
    double x;
    double y;

    ifstream entrada;
    entrada.open(nome.c_str());

    double xmin;
    double ymin;

    entrada >> x >> y;
    xmin = x;
    ymin = y;

    while (!entrada.eof())
    {
        entrada >> x >> y;
        if (y < ymin)
        {
            xmin = x;
            ymin = y;
        }
    }

    entrada.close();

    if (tipo == "x") return xmin;
    else return ymin;
}

void salvaIntervalos (string lista)
{
    ifstream flista;
    ofstream saida;

    string nome_saida = nameLabel (lista, ".txt", "intervalos");

    flista.open(lista.c_str());
    saida.open(nome_saida.c_str());

    string arquivo;
    string old;
    old = "-1";

    while (!flista.eof())
    {
        flista >> arquivo;
        if (arquivo != old){
        saida << scientific << "xrange [" << valorMinimo (arquivo, "x") << ", " << valorMaximo (arquivo, "x") << "]  ";
        saida << "yrange [" << valorMinimo (arquivo, "y") << ", " << valorMaximo (arquivo, "y") << "]  ";
        saida << endl;
        }
        old = arquivo;
    }
    flista.close();
    saida.close();
}

void imprimeArray (double *vetor, int size)
{
    for (int i = 0; i < size; i++)
        cout << scientific << "[" << i << "] = " << vetor[i] << endl;
    cout << endl;
}

void inicializaArray (double *vetor, int size, double valor)
{
    for (int i = 0; i < size; i++)
        vetor[i] = valor;
}

void openIfstream (ifstream &entrada, string nome)
{
    entrada.open(nome.c_str());
    if (entrada.fail())
    {
        cout << "O arquivo " << nome << " nao existe\n";
        exit(0);
    }
}

string ajustaSubstring (string sub, string caractere)
{
    int i;
    for (i = 0; i < sub.length(); i++)
    {
        if (sub.find(caractere) == 0)
            sub = sub.substr (sub.find(caractere)+1, sub.length()-sub.find(caractere)-1);
    }

    return sub;
}

string leAntesCaractere (string linha, string caractere, int maximo, int vez) //se vez > maximo: captura o restante da string
{
    string dado;
    string sub;
    int i;

    if (vez <= maximo){

    for (i = 0; i < vez; i++)
    {
        dado = linha.substr (0, linha.find(caractere));
        sub = linha.substr (linha.find(caractere)+1, linha.length()-linha.find(caractere)-1);
        linha = ajustaSubstring (sub, caractere);
    }

    }
    else
    {
        vez = maximo;
        for (i = 0; i < vez; i++)
        {
            dado = linha.substr (0, linha.find(caractere));
            sub = linha.substr (linha.find(caractere)+1, linha.length()-linha.find(caractere)-1);
            linha = ajustaSubstring (sub, caractere);
        }
        dado = linha;
    }

    dado = ajustaSubstring (dado, caractere);

    return dado;
}

int totalLines (ifstream &entrada, int caso)//caso == 1: despreza linhas vazias
{
    int total = 0;
    string linha;

    while (!entrada.eof())
    {
        getline (entrada, linha);
        if (caso == 1){
        if (linha.length() > 1)
            total++;
        else if (linha.length() == 1)
            if (linha != " ") total++;
        }
        else total++;

    }
//    entrada.close();
    return total;
}

int totalCaracteres (string s, string key)
{
    int total = 0;
    int valor = -1;
    do
    {
        valor = s.find(key);
        if (valor == -1)
            return total;
        else
        {
            s = s.substr (valor+1, s.length()-1);
            total++;
        }
    }while (valor != -1);
}

string alteraCaractere (string s, string caractere, string novo)
{
    int t = totalCaracteres (s, caractere);
    // cout << "tot:" << t << endl;
    string aux;

    string new_string;
    aux = leAntesCaractere (s, caractere, t, 1);
    new_string = aux;
    new_string += novo;

    int i;
    for (i = 2; i <= t; i++)
    {
        aux = leAntesCaractere (s, caractere, t, i);
        new_string += aux;
        new_string += novo;
        // cout << "i:" << i << ";";
        // cout << "aux:" << aux << ";";
        // cout << "new_string:" << new_string << endl;
    }
    aux = leAntesCaractere (s, caractere, t, i);
    new_string += aux;

    return new_string;
}

void reload (ifstream &file, string nome)
{
    file.close();
    openIfstream (file, nome);
}

void normaliza (string nome, double valor)
{
    ofstream saida;
    string nomeSaida;
    nomeSaida = nome.substr (0, nome.length() - 4);
    nomeSaida += "_norm";
    nomeSaida += nome.substr (nome.length()-4, nome.length());

    saida.open (nomeSaida.c_str());

    ifstream entrada;
    openIfstream (entrada, nome);
    int total = totalLines (entrada, 1);

    reload (entrada, nome);

    double x;
    double y;

    int i;

    for (i = 0; i < total; i++)
    {
        entrada >> x >> y;
        saida << x << " " << y/valor << endl;
    }

    entrada.close();
    saida.close();
}
