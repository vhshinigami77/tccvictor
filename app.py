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

    # 1. Salvar o áudio enviado
    audio.save(wav_path)

    # 2. Converter WAV para DAT com sox (PCM 44100Hz mono)
    try:
        subprocess.run([
            'sox', wav_path, '-r', '44100', dat_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Erro ao converter com sox: {e}'}), 500

    # 3. Compilar 'saida'
    try:
        subprocess.run([
            'g++', 'gera_espectro4_ok.cpp', 'nilton_basics_ok.cpp', '-o', 'saida'
        ], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Erro ao compilar gera_espectro4_ok.cpp: {e}'}), 500

    # 4. Executar './saida <uid> <dat_path> 0.5'
    try:
        subprocess.run(['./saida', uid, dat_path, '0.5'], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Erro ao executar ./saida: {e}'}), 500

    # 5. Compilar 'shownote.cpp'
    try:
        subprocess.run(['g++', 'shownote.cpp', '-o', 'resultado'], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Erro ao compilar shownote.cpp: {e}'}), 500

    # 6. Executar './resultado resultado_<uid>.txt'
    try:
        subprocess.run(['./resultado', f'resultado_{uid}.txt'], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Erro ao executar ./resultado: {e}'}), 500

    # 7. Ler nota detectada
    try:
        with open('nota.txt') as f:
            nota = f.read().strip()
    except Exception as e:
        nota = 'Erro ao ler nota.txt'
        print(e)

    # 8. Ler frequência de resultado_saida.txt
    freq = None
    try:
        with open(f'resultado_{uid}.txt') as f:
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
