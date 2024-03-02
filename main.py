from flask import Flask, request, jsonify
import speech_recognition as sr
from flask_cors import CORS
from convert import convert_to_wav
from gradio_client import Client
import uuid
import os
app = Flask(__name__)
client = Client("Namit2111/Salesforce-blip-image-captioning-base")

CORS(app)

def generate_random_filename():
    random_filename = str(uuid.uuid4()) + ".jpg"
    return random_filename

def generate_random_filename_aud():
    random_filename = str(uuid.uuid4()) + ".wav"
    return random_filename

def audio_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Converting audio to text...")
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

@app.route('/')
def home():
    return jsonify('Hello, World!')

@app.route('/audio', methods=['POST'])
def predict_audio():
    try:
        audio_file = request.files['file']
        name = generate_random_filename_aud()
        audio_file.save(name)
        print("saved")
         # Save the file temporarily
        name2 = generate_random_filename_aud()
        convert_to_wav(name,name2)
        result = audio_to_text(name2)
        os.remove(name)
        os.remove(name2)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/photo', methods=['POST'])
def vid():
    try:
        photo_file = request.files['file']
        name = generate_random_filename()
        photo_file.save(name)
        result = client.predict(
            name,	# filepath  in 'Input Image' Image component
            api_name="/predict"
    )   
        print(result)
        os.remove(name)
        return jsonify({'result': result})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
