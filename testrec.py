import pyaudio
import wave
import sounddevice
import sys

def gravar_audio(seconds, fs):
    audio = pyaudio.PyAudio()
    stream = audio.open(
        input=True,
        format=pyaudio.paInt16,
        channels=1,
        rate=fs,
        frames_per_buffer=1024,
    )
    frames = []

    for i in range(0, int(fs / 1024 * seconds)):
        bloco = stream.read(1024)
        frames.append(bloco)

    stream.start_stream()
    stream.close()
    audio.terminate()
    arquivo_final = wave.open('saida.wav', 'wb')
    arquivo_final.setnchannels(1)
    arquivo_final.setframerate(fs)
    arquivo_final.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    arquivo_final.writeframes(b"".join(frames))
    arquivo_final.close()

