from flask import Flask
from flask import request
from flask import render_template, send_from_directory
from uuid import uuid4
from pydub import AudioSegment


import base64
import json
import openai
import os

app = Flask(__name__)

OPENAI_KEY = "" #INGRESAR KEY DE OPENAI
OPENAI_API_URL = "https://api.openai.com/v1"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/resources/<path:path>', methods=['GET'])
def resources(path):
    return send_from_directory('resources', path)


@app.route('/transcribe', methods=['POST'])
def post_audio_file():
    # You must complete the full implementation for this
    # primero se agarra el dato que necesitamos con el metodo get_data que viene en flask
    audioFile = request.get_data()
    decoded_text = audioFile.decode('utf-8')
    json_data = json.loads(decoded_text)
    mensaje = json_data['data']

    print(mensaje)

    audioOut = base64.b64decode(mensaje)

    # Ruta temporal para guardar el archivo
    audio_file_path = f"VOZ\prueba.webm"

    # Guardar el archivo de audio
    with open(audio_file_path, 'wb') as audio_file:
        audio_file.write(audioOut)
        

    # Realizar la transcripción utilizando el archivo de audio
    openai.api_key = OPENAI_KEY
    with open(audio_file_path, 'rb') as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    #os.remove(audio_file_path)
    return transcript


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
