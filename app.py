from flask import Flask, request, send_from_directory, jsonify
import os
import subprocess
import uuid
import soundfile as sf

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
    wav_path = os.path.join(UPLOAD_FOLDER, f'{uid}.wav')
    dat_path = os.path.join(UPLOAD_FOLDER, f'{uid}.dat')

    audio_file.save(wav_path)

    # Convert WAV to DAT using sox
    subprocess.run(['sox', wav_path, '-r', '44100', dat_path])

    # Run C++ spectral analysis
    subprocess.run(['./saida', uid, dat_path, '0.5'])

    # Run note detector
    subprocess.run(['./resultado'])

    # Read detected note
    with open('nota.txt') as f:
        nota = f.read().strip()

    return jsonify({ 'nota': nota })

if __name__ == '__main__':
    app.run()

