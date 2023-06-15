from flask import Flask
from flask import request
from flask import render_template, send_from_directory
from uuid import uuid4

import base64
import json
import openai
import os

app = Flask(__name__)

OPENAI_KEY = "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"
#OPENAI_API_URL = # Must complete this part

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/resources/<path:path>', methods=['GET'])
def resources(path):
    return send_from_directory('resources', path)

@app.route('/transcribe', methods=['POST'])
def post_audio_file():
    # You must complete the full implementation for this
    #primero se agarra el dato que necesitamos con el metodo get_data que viene en flask
    audioFile = request.get_data()
    #con ayuda de base64 vamos a decodificar el archivo llegado
    audioOut = base64.b64decode(audioFile)
    
    
    audio_file_path = f"D:\\SaveAudio\\prueba.mp3"  # Ruta temporal para guardar el archivo
    
    audio_prueba = f"D:\\SaveAudio\\prueba2.mp3"
    # Guardar el archivo de audio
    with open(audio_file_path, 'wb') as audio_file:
        audio_file.write(audioOut)

    # Realizar la transcripción utilizando el archivo de audio
    openai.api_key = OPENAI_KEY
    with open(audio_file_path, 'rb') as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        
    os.remove(audio_file_path)
    return render_template("index.html", transcription= transcript["text"])

if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
