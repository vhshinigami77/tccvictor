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

    original_path = os.path.join(UPLOAD_FOLDER, f'{uid}_original')
    wav_path = os.path.join(UPLOAD_FOLDER, f'{uid}.wav')
    dat_path = os.path.join(UPLOAD_FOLDER, f'{uid}.dat')

    # Salva o arquivo original com extensão para o ffmpeg reconhecer
    filename = audio.filename
    original_path += os.path.splitext(filename)[1]
    audio.save(original_path)

    # 1. Converte o original para WAV 44.1kHz mono com ffmpeg
    subprocess.run([
        'ffmpeg', '-y', '-i', original_path,
        '-ar', '44100', '-ac', '1',
        wav_path
    ], check=True)

    # 2. Usa sox para converter WAV para arquivo raw PCM 16 bits (.dat)
    subprocess.run([
        'sox', wav_path,
        '-r', '44100',
        '-c', '1',
        '-b', '16',
        '-e', 'signed-integer',
        '-t', 'raw',
        dat_path
    ], check=True)

    # 3. Compilar o programa principal (gera espectro)
    subprocess.run([
        'g++', 'gera_espectro4_ok.cpp', 'nilton_basics_ok.cpp', '-o', 'saida'
    ], check=True)

    # 4. Executar análise espectral
    subprocess.run(['./saida', uid, dat_path, '0.5'], check=True)

    # 5. Compilar o programa de resultado (mostra nota)
    subprocess.run(['g++', 'shownote.cpp', '-o', 'resultado'], check=True)

    # 6. Executar programa que gera o arquivo de nota
    subprocess.run(['./resultado', f'resultado_{uid}.txt'], check=True)

    # 7. Ler nota do arquivo 'nota.txt'
    try:
        with open('nota.txt') as f:
            nota = f.read().strip()
    except Exception as e:
        nota = 'Erro ao ler nota.txt'
        print(e)

    # 8. Ler frequência do arquivo resultado_saida.txt
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
