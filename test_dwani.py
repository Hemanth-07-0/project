#!/usr/bin/env python3
"""
Test script for Dwani AI integration
"""

import sys
import os

# Add backend-api to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend-api'))

try:
    from dwani import transcribe_audio
    print("✅ Dwani module imported successfully")
    print(f"📡 API Base URL: https://dwani-dwani-api.hf.space")
    print(f"📧 Email: adithyaadithya459@gmail.com")
    print(f"🔑 API Key: adithyadithya459@gmail.com_dwani")
    print()
    
    # Test the configuration
    print("🧪 Testing Dwani AI configuration...")
    print("Note: This will only work with an actual audio file")
    
except ImportError as e:
    print(f"❌ Error importing Dwani module: {e}")

# Now let's start the Flask server
try:
    print("\n🚀 Starting Flask server...")
    os.chdir('backend-api')
    
    from app import app
    print("✅ Flask app imported successfully")
    
    print("🌐 Starting server on http://localhost:5000")
    print("🎤 Voice API available at: http://localhost:5000/voice/transcribe")
    print("📋 Supported languages: English (en), Hindi (hi), Kannada (kn)")
    print("=" * 60)
    print("Server is running... Press Ctrl+C to stop")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except Exception as e:
    print(f"❌ Error starting server: {e}")
    import traceback
    traceback.print_exc()
