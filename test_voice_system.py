#!/usr/bin/env python3
"""
Test script for the voice-based patient record lookup system
"""

import requests
import json
import io
import wave
import struct
import math

def create_dummy_audio_file():
    """Create a dummy audio file for testing"""
    # Create a simple sine wave audio file
    sample_rate = 44100
    duration = 2  # seconds
    frequency = 440  # Hz (A note)
    
    # Generate sine wave
    frames = []
    for i in range(int(sample_rate * duration)):
        value = int(32767 * math.sin(2 * math.pi * frequency * i / sample_rate))
        frames.append(struct.pack('<h', value))
    
    # Create WAV file in memory
    audio_buffer = io.BytesIO()
    with wave.open(audio_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(frames))
    
    audio_buffer.seek(0)
    return audio_buffer

def test_voice_health():
    """Test the voice service health endpoint"""
    print("🔍 Testing voice service health...")
    try:
        response = requests.get('http://localhost:5000/voice/health')
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Voice service is online: {result}")
            return True
        else:
            print(f"❌ Voice service health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to voice service: {e}")
        return False

def test_voice_transcription_and_search():
    """Test the voice transcription and patient search functionality"""
    print("\n🎤 Testing voice transcription and patient search...")
    
    try:
        # Create dummy audio file
        audio_file = create_dummy_audio_file()
        
        # Prepare the request
        files = {'audio': ('test_audio.wav', audio_file, 'audio/wav')}
        data = {'language': 'en'}
        
        # Make the request
        response = requests.post(
            'http://localhost:5000/voice/transcribe-and-search',
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Transcription successful!")
            print(f"📝 Transcribed text: '{result.get('text', 'N/A')}'")
            print(f"🌍 Language: {result.get('language', 'N/A')}")
            
            matching_records = result.get('matching_records', [])
            print(f"📋 Found {len(matching_records)} patient(s) with records")
            
            for i, patient in enumerate(matching_records, 1):
                print(f"\n👤 Patient {i}: {patient.get('patient_name', 'Unknown')}")
                records = patient.get('records', [])
                print(f"   📁 Records: {len(records)} file(s)")
                
                for j, record in enumerate(records, 1):
                    print(f"   📄 {j}. {record.get('file_name', 'Unknown')} ({record.get('file_type', 'Unknown')})")
            
            return True
        else:
            print(f"❌ Transcription failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing transcription: {e}")
        return False

def test_patient_records():
    """Test if patient records exist in the database"""
    print("\n📊 Testing patient records in database...")
    
    try:
        # Test the records endpoint
        response = requests.get('http://localhost:5000/records/')
        if response.status_code == 200:
            print("✅ Records endpoint is accessible")
            return True
        else:
            print(f"❌ Records endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing records: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Starting Voice-Based Patient Record Lookup System Tests")
    print("=" * 60)
    
    # Test 1: Voice service health
    health_ok = test_voice_health()
    
    # Test 2: Patient records
    records_ok = test_patient_records()
    
    # Test 3: Voice transcription and search
    voice_ok = test_voice_transcription_and_search()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY:")
    print(f"   Voice Service Health: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"   Patient Records:      {'✅ PASS' if records_ok else '❌ FAIL'}")
    print(f"   Voice Search:         {'✅ PASS' if voice_ok else '❌ FAIL'}")
    
    if all([health_ok, records_ok, voice_ok]):
        print("\n🎉 All tests passed! The system is ready for use.")
        print("\nTo test the frontend:")
        print("1. Open public/patient-health-records.html in your browser")
        print("2. Click 'START RECORDING' and speak (or just click for simulation)")
        print("3. The system will show matching patient records")
    else:
        print("\n⚠️  Some tests failed. Check the backend server and database.")

if __name__ == '__main__':
    main()
