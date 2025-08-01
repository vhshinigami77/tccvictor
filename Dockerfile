FROM python:3.10-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    sox \
    libsox-fmt-all \
    g++ \
 && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Compila os binários C++
#RUN chmod +x build.sh && ./build.sh

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta da aplicação
EXPOSE 8080

# Comando para iniciar o Flask
CMD ["python", "app.py"]
