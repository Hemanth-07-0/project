#!/usr/bin/env python3
"""
Start script for Visbo Healthcare Backend with Dwani AI Integration
"""

import os
import sys
import subprocess

def main():
    print("🚀 Starting Visbo Healthcare Backend with Dwani AI...")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend-api')
    
    if not os.path.exists(backend_dir):
        print("❌ Backend directory not found!")
        return
    
    os.chdir(backend_dir)
    
    # Check if virtual environment exists
    venv_dir = os.path.join(backend_dir, 'venv')
    if not os.path.exists(venv_dir):
        print("⚠️  Virtual environment not found. Creating one...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'])
    
    # Determine the correct Python executable
    if os.name == 'nt':  # Windows
        python_exe = os.path.join(venv_dir, 'Scripts', 'python.exe')
        pip_exe = os.path.join(venv_dir, 'Scripts', 'pip.exe')
    else:  # Unix/Linux/Mac
        python_exe = os.path.join(venv_dir, 'bin', 'python')
        pip_exe = os.path.join(venv_dir, 'bin', 'pip')
    
    # Install requirements
    print("📦 Installing requirements...")
    subprocess.run([pip_exe, 'install', '-r', 'requirements.txt'])
    
    # Start the server
    print("🎤 Starting Dwani AI Voice-to-Text Backend...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🎯 Voice API endpoint: http://localhost:5000/voice/transcribe")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        subprocess.run([python_exe, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
