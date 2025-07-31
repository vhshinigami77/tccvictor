# Usa Python 3.10 slim como base
FROM python:3.10-slim

# Atualiza repositório e instala sox + todos os formatos
RUN apt-get update && apt-get install -y sox libsox-fmt-all && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos da aplicação para dentro do container
COPY . /app

# Instala dependências Python (coloque seu requirements.txt na raiz)
RUN pip install --no-cache-dir -r requirements.txt

# Expõe porta 8080 (ou a porta que usar no app.py)
EXPOSE 8080

# Comando para rodar a aplicação
CMD ["python", "app.py"]
