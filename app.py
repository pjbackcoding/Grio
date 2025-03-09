"""
Main application file for the Interview Assistant.
This file contains the Flask application and routes.
"""

import os
import time
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import speech_recognition as sr
from openai import OpenAI

# Configuration settings
DEFAULT_SYSTEM_PROMPT = """
You are an AI assistant helping a job candidate during an interview. 
Your task is to provide helpful, concise, and professional responses to interview questions.
Focus on showcasing the candidate's skills and experience in the best possible light.
Provide specific examples and achievements when possible.
Keep responses between 100-200 words unless the question requires a more detailed answer.
Avoid generic answers and try to personalize responses based on the context of the question.
"""

# API settings
MAX_TOKENS = 500
TEMPERATURE = 0.7
MODEL = "gpt-3.5-turbo"
WHISPER_MODEL = "whisper-1"

# Web interface settings
HOST = "0.0.0.0"
PORT = 5001  # Changed from 5000 to avoid port conflict
DEBUG = True

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize speech recognizer
recognizer = sr.Recognizer()

@app.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Transcribe audio using OpenAI's Whisper API.
    Supports multiple languages via the 'language' parameter.
    
    Returns:
        JSON response with transcribed text
    """
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    
    # Get language from form data, default to English
    language = request.form.get('language', 'en')
    
    try:
        # Save the audio file temporarily
        temp_filename = f"temp_audio_{int(time.time())}.wav"
        audio_file.save(temp_filename)
        
        # Prepare language parameter (Whisper uses 2-letter codes)
        whisper_lang = language.split('-')[0] if '-' in language else language
        
        # Transcribe using OpenAI's Whisper API with language hint
        with open(temp_filename, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=audio_file,
                language=whisper_lang  # Pass the language code to Whisper
            )
        
        # Remove temporary file
        os.remove(temp_filename)
        
        return jsonify({'text': transcript.text})
    
    except Exception as e:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-response', methods=['POST'])
def generate_response():
    """
    Generate a response to an interview question using OpenAI's GPT model.
    
    Returns:
        JSON response with AI-generated answer
    """
    data = request.json
    if not data or 'question' not in data:
        return jsonify({'error': 'No question provided'}), 400
    
    question = data['question']
    job_role = data.get('job_role', '')
    context = data.get('context', '')
    
    # Customize the system prompt based on job role if provided
    system_prompt = DEFAULT_SYSTEM_PROMPT
    if job_role:
        system_prompt += f"\nThe candidate is applying for a {job_role} position."
    if context:
        system_prompt += f"\nAdditional context: {context}"
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        
        answer = response.choices[0].message.content
        return jsonify({'answer': answer})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transcribe-from-mic', methods=['POST'])
def transcribe_from_mic():
    """
    Transcribe audio from microphone using SpeechRecognition library.
    This is an alternative to the Whisper API for local speech recognition.
    Supports multiple languages via the 'language' parameter.
    
    Returns:
        JSON response with transcribed text
    """
    try:
        # Get language from request, default to English
        data = request.get_json(silent=True) or {}
        language = data.get('language', 'en-US')
        
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        
        # Use Google's speech recognition with specified language
        text = recognizer.recognize_google(audio, language=language)
        return jsonify({'text': text})
    
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f'Error with the speech recognition service: {e}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable is not set.")
        print("Please set it in a .env file or in your environment variables.")
    
    print("\nInterviewer Assistant is running!")
    print("Both microphone input and file uploads are supported.")
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
