#!/usr/bin/env python
# Script to start both frontend and backend servers

import os
import sys
import subprocess
import webbrowser
import time
from threading import Thread

# Configuration
BACKEND_DIR = os.path.join(os.path.dirname(__file__), 'backend-api')
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'public')
BACKEND_PORT = 5000
FRONTEND_PORT = 8000

def start_backend():
    """Start the backend Flask server"""
    print("Starting backend server...")
    os.chdir(BACKEND_DIR)
    
    # Check if virtual environment exists
    venv_python = os.path.join(BACKEND_DIR, 'venv', 'Scripts', 'python.exe')
    if not os.path.exists(venv_python):
        print("Virtual environment not found. Please set up the backend first.")
        print("See README.md for setup instructions.")
        return False
    
    # Run the backend server
    try:
        subprocess.Popen([venv_python, 'run.py'])
        print(f"Backend server running at http://localhost:{BACKEND_PORT}")
        return True
    except Exception as e:
        print(f"Error starting backend server: {e}")
        return False

def start_frontend():
    """Start the frontend server using Python's HTTP server"""
    print("Starting frontend server...")
    os.chdir(FRONTEND_DIR)
    
    # Run the frontend server
    try:
        if sys.platform.startswith('win'):
            # Hide console window on Windows
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(
                [sys.executable, '-m', 'http.server', str(FRONTEND_PORT)],
                startupinfo=startupinfo
            )
        else:
            subprocess.Popen([sys.executable, '-m', 'http.server', str(FRONTEND_PORT)])
        
        print(f"Frontend server running at http://localhost:{FRONTEND_PORT}")
        return True
    except Exception as e:
        print(f"Error starting frontend server: {e}")
        return False

def open_browser():
    """Open the browser to the frontend URL"""
    time.sleep(2)  # Wait for servers to start
    webbrowser.open(f"http://localhost:{FRONTEND_PORT}")

if __name__ == "__main__":
    print("Starting Visbo Healthcare Platform...")
    
    # Start backend server
    backend_started = start_backend()
    
    # Start frontend server
    frontend_started = start_frontend()
    
    if backend_started and frontend_started:
        print("\nVisbo Healthcare Platform is running!")
        print(f"- Frontend: http://localhost:{FRONTEND_PORT}")
        print(f"- Backend API: http://localhost:{BACKEND_PORT}")
        
        # Open browser
        Thread(target=open_browser).start()
        
        print("\nPress Ctrl+C to stop the servers.")
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping servers...")
    else:
        print("\nFailed to start all servers. Please check the errors above.")