from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import subprocess

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    return 'Servidor rodando com compilação dinâmica.'

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    audio = request.files['audio']
    uid = str(uuid.uuid4())

    wav_path = os.path.join(UPLOAD_FOLDER, f'{uid}.wav')
    dat_path = os.path.join(UPLOAD_FOLDER, f'{uid}.dat')

    # 1. Salvar o áudio
    audio.save(wav_path)

    # 2. Converter WAV para DAT (PCM 44100Hz mono)
    subprocess.run([
        'ffmpeg', '-y', '-i', wav_path,
        '-f', 's16le', '-ar', '44100', '-ac', '1',
        dat_path
    ], check=True)

    # 3. Compilar 'saida'
    subprocess.run([
        'g++', 'gera_espectro4_ok.cpp', 'nilton_basics_ok.cpp', '-o', 'saida'
    ], check=True)

    # 4. Executar './saida <uid> <dat_path> 0.5'
    subprocess.run(['./saida', uid, dat_path, '0.5'], check=True)

    # 5. Compilar 'shownote.cpp' → 'resultado'
    subprocess.run(['g++', 'shownote.cpp', '-o', 'resultado'], check=True)

    # 6. Executar './resultado'
    subprocess.run(['./resultado', f'resultado_{uid}.txt'], check=True)
    # 7. Ler nota.txt
    try:
        with open('nota.txt') as f:
            nota = f.read().strip()
    except Exception as e:
        nota = 'Erro ao ler nota.txt'
        print(e)

    # 8. Ler frequência de resultado_saida.txt
    freq = None
    try:
        with open('resultado_saida.txt') as f:
            line = f.readline()
            freq = float(line.split()[0]) if line else None
    except Exception as e:
        print("Erro ao ler resultado_saida.txt:", e)

    return jsonify({
        'nota': nota,
        'frequencia': freq
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
