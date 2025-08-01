from flask import Flask, request, send_from_directory, jsonify
import os
import subprocess
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return 'No audio file', 400

    audio_file = request.files['audio']
    uid = str(uuid.uuid4())
    original_path = os.path.join(UPLOAD_FOLDER, f'{uid}_original')
    wav_path = os.path.join(UPLOAD_FOLDER, f'{uid}.wav')
    dat_path = os.path.join(UPLOAD_FOLDER, f'{uid}.dat')

    # Salva o arquivo original (pode ser opus/webm/etc.)
    audio_file.save(original_path)

    # Converte para WAV 44.1kHz com ffmpeg
    result = subprocess.run(['ffmpeg', '-y', '-i', original_path, '-ar', '44100', wav_path], capture_output=True)

    if result.returncode != 0:
        return f"Erro ao converter áudio com ffmpeg: {result.stderr.decode()}", 500

    # Converte WAV para .dat (você pode fazer isso com sox ou continuar usando ffmpeg se preferir)
    subprocess.run(['ffmpeg', '-y', '-i', wav_path, '-f', 's16le', '-acodec', 'pcm_s16le', dat_path])

    # Garante que o arquivo .dat foi criado
    if not os.path.exists(dat_path):
        return f"O arquivo {dat_path} não foi gerado corretamente.", 500

    # Executa o binário de análise espectral
    subprocess.run(['./saida', uid, dat_path, '0.5'])

    # Executa o detector de notas
    subprocess.run(['./resultado'])

    # Lê nota musical
    try:
        with open('nota.txt') as f:
            nota = f.read().strip()
    except FileNotFoundError:
        nota = 'ERRO: nota.txt não encontrado'

    return jsonify({'nota': nota})
