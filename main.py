import os
import testrec

#forma mais simples do programa
#tentar modularizar pra fazer um main()
def main():
    seconds = float(input("Forneça o tempo para fazer a deteção da nota: "))
    fs = int(input("Forneça a frequência de amostragem: "))
    try:
        while(True):
            testrec.gravar_audio(seconds, fs)
            os.system("sox saida.wav -r {} saida.dat".format(fs))
            os.system("g++ gera_espectro4_ok.cpp nilton_basics_ok.o -o saida")
            os.system("./saida saida saida.dat 0.5")
            os.system("g++ shownote.cpp -o resultado")
            os.system("./resultado")        
    except KeyboardInterrupt:
        pass
main()