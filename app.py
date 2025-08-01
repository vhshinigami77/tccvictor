from flask import Flask, request, jsonify
import os
import uuid
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # caminho absoluto do diretório atual

@app.route('/')
def index():
    return "Servidor rodando."

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return 'No audio file', 400

    audio_file = request.files['audio']
    uid = str(uuid.uuid4())

    wav_path = os.path.join(BASE_DIR, UPLOAD_FOLDER, f'{uid}.wav')
    dat_path = os.path.join(BASE_DIR, UPLOAD_FOLDER, f'{uid}.dat')

    # Salva o arquivo recebido
    audio_file.save(wav_path)

    # Converte WAV para DAT (raw PCM)
    subprocess.run([
        'ffmpeg', '-y', '-i', wav_path,
        '-f', 's16le', '-ar', '44100', '-ac', '1',
        dat_path
    ], check=True)

    # Caminhos absolutos para os binários
    saida_bin = os.path.join(BASE_DIR, 'saida')
    resultado_bin = os.path.join(BASE_DIR, 'resultado')

    # Executa seu programa C++ que gera resultado_saida.txt
    subprocess.run([saida_bin, uid, dat_path, '0.5'], check=True)

    # Executa o shownote que gera nota.txt
    subprocess.run([resultado_bin], check=True)

    # Inicializa valores padrão
    nota = "Desconhecida"
    frequencia = None

    # Lê a nota detectada
    nota_path = os.path.join(BASE_DIR, 'nota.txt')
    try:
        with open(nota_path, 'r') as f:
            nota = f.read().strip()
    except Exception as e:
        print("Erro ao ler nota.txt:", e)

    # Lê frequência dominante (supondo que seu programa grava em resultado_saida.txt)
    resultado_saida_path = os.path.join(BASE_DIR, 'resultado_saida.txt')
    try:
        with open(resultado_saida_path, 'r') as f:
            line = f.readline()
            parts = line.split()
            if len(parts) >= 1:
                frequencia = float(parts[0])
    except Exception as e:
        print("Erro ao ler resultado_saida.txt:", e)

    return jsonify({
        'nota': nota,
        'frequencia': frequencia
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
