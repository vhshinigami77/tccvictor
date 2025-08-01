from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import subprocess

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

    audio_file.save(wav_path)

    subprocess.run([
        'ffmpeg', '-y', '-i', wav_path,
        '-f', 's16le', '-ar', '44100', '-ac', '1',
        dat_path
    ], check=True)

    subprocess.run([os.path.join(BASE_DIR, 'saida'), uid, dat_path, '0.5'], check=True)
    subprocess.run([os.path.join(BASE_DIR, 'resultado')], check=True)

    nota = "Desconhecida"
    frequencia = None

    try:
        with open(os.path.join(BASE_DIR, 'nota.txt'), 'r') as f:
            nota = f.read().strip()
    except Exception as e:
        print("Erro ao ler nota.txt:", e)

    try:
        with open(os.path.join(BASE_DIR, 'resultado_saida.txt'), 'r') as f:
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
