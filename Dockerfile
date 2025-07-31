FROM python:3.10-slim

# Instala sox e compilador C++ (g++)
RUN apt-get update && apt-get install -y \
    sox \
    libsox-fmt-all \
    g++ \
 && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Dá permissão e roda o script de build dos binários C++
RUN chmod +x build.sh && ./build.sh

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta da aplicação Flask
EXPOSE 8080

# Comando para rodar a aplicação
CMD ["python", "app.py"]
