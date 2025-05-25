#!/usr/bin/env python3
"""
Simple Flask server for Dwani AI Voice-to-Text testing
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import sys

# Add backend-api to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend-api'))

try:
    from dwani import transcribe_audio
    DWANI_AVAILABLE = True
    print("✅ Dwani AI module loaded successfully")
except ImportError as e:
    DWANI_AVAILABLE = False
    print(f"❌ Dwani AI module not available: {e}")

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'webm', 'm4a', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return jsonify({
        'status': 'online',
        'message': 'Dwani AI Voice-to-Text Server',
        'dwani_available': DWANI_AVAILABLE
    })

@app.route('/voice/health')
def voice_health():
    return jsonify({
        'success': True,
        'service': 'Dwani AI Voice Transcription',
        'status': 'online',
        'dwani_available': DWANI_AVAILABLE
    })

@app.route('/voice/languages')
def get_languages():
    return jsonify({
        'success': True,
        'languages': [
            {'code': 'en', 'name': 'English'},
            {'code': 'hi', 'name': 'Hindi'},
            {'code': 'kn', 'name': 'Kannada'}
        ]
    })

@app.route('/voice/transcribe', methods=['POST'])
def transcribe_voice():
    try:
        # Check if Dwani is available
        if not DWANI_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'Dwani AI module not available'
            }), 500
        
        # Check if audio file is present
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No audio file provided'
            }), 400
        
        file = request.files['audio']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Get language parameter
        language = request.form.get('language', 'en')
        supported_languages = ['en', 'hi', 'kn']
        if language not in supported_languages:
            language = 'en'
        
        print(f"📝 Processing audio file: {file.filename}")
        print(f"🌍 Language: {language}")
        print(f"📊 File size: {len(file.read())} bytes")
        file.seek(0)  # Reset file pointer
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        try:
            print(f"🎤 Sending to Dwani AI...")
            # Transcribe using Dwani AI
            transcribed_text = transcribe_audio(temp_file_path, language)
            print(f"📄 Transcription result: {transcribed_text}")
            
            # Check if transcription was successful
            if transcribed_text.startswith("Error:"):
                return jsonify({
                    'success': False,
                    'error': transcribed_text
                }), 500
            
            return jsonify({
                'success': True,
                'text': transcribed_text,
                'language': language,
                'message': 'Audio transcribed successfully using Dwani AI'
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                print(f"🗑️ Cleaned up temporary file")
    
    except Exception as e:
        print(f"❌ Error in transcription: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Dwani AI Voice-to-Text Server")
    print("=" * 50)
    print(f"📡 Server URL: http://localhost:5000")
    print(f"🎤 Transcribe endpoint: http://localhost:5000/voice/transcribe")
    print(f"🌍 Supported languages: English, Hindi, Kannada")
    print(f"✅ Dwani AI Available: {DWANI_AVAILABLE}")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
