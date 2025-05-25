# 🎤 Dwani AI Voice-to-Text Integration

This project now includes **Dwani AI** integration for advanced multilingual voice-to-text conversion supporting English, Hindi, and Kannada.

## 🚀 Quick Start

### 1. Start the Backend Server
```bash
python start_backend.py
```

### 2. Open the Frontend
Open `public/patient-health-records.html` in your browser

### 3. Use Voice-to-Text
1. Select your language (English/Hindi/Kannada)
2. Click "🎤 START RECORDING"
3. Speak clearly into your microphone
4. Click "⏹️ STOP RECORDING"
5. Wait for Dwani AI to process and display the text

## 🔧 Technical Architecture

### Backend (Python Flask)
- **Location**: `backend-api/`
- **Main File**: `app.py`
- **Voice Route**: `routes/voice.py`
- **Dwani Integration**: `dwani.py`

### Frontend (HTML/JavaScript)
- **Location**: `public/patient-health-records.html`
- **Features**: Real-time recording, language selection, Dwani AI integration

### API Endpoints
- `POST /voice/transcribe` - Convert audio to text
- `GET /voice/languages` - Get supported languages
- `GET /voice/health` - Health check

## 🎯 Features

### ✨ Voice Recording
- High-quality audio recording using MediaRecorder API
- Real-time status updates
- Error handling and recovery

### 🌍 Multilingual Support
- **English** (en) - Primary language
- **Hindi** (hi) - Devanagari script support
- **Kannada** (kn) - Regional language support

### 🔄 Processing Pipeline
1. **Audio Capture** - Browser records audio
2. **Upload** - Audio sent to backend
3. **Dwani AI** - Advanced speech recognition
4. **Display** - Transcribed text shown to user

## 🛠️ Configuration

### Dwani AI Settings
Edit `backend-api/dwani.py`:
```python
DWANI_API_BASE_URL = "https://dwani-dwani-api.hf.space"
EMAIL_ID = "your-email@example.com"
DWANI_API_KEY = "your-dwani-api-key"
```

### Frontend Settings
Edit `public/patient-health-records.html`:
```javascript
const API_BASE_URL = 'http://localhost:5000';
```

## 📋 Requirements

### Backend Dependencies
- Flask
- Flask-CORS
- requests
- SQLAlchemy

### Browser Requirements
- Modern browser with MediaRecorder API support
- Microphone access permission
- Internet connection for Dwani AI

## 🔍 Troubleshooting

### Common Issues

1. **Microphone Access Denied**
   - Allow microphone permission in browser
   - Check browser security settings

2. **Backend Connection Failed**
   - Ensure backend server is running on port 5000
   - Check CORS settings

3. **Dwani AI Error**
   - Verify API key and credentials
   - Check internet connection
   - Ensure audio file format is supported

### Debug Mode
Open browser developer tools (F12) to see detailed logs:
- Audio recording status
- Backend communication
- Dwani AI responses

## 🎨 UI Features

### Visual Indicators
- **Blue Background**: Recording in progress
- **Yellow Background**: Processing audio
- **Green Background**: Transcription successful
- **Red Background**: Error occurred

### Status Messages
- ✅ Success indicators
- ❌ Error messages
- 🎤 Recording status
- 🔄 Processing updates

## 🔐 Security Notes

- Audio data is temporarily stored during processing
- Files are automatically cleaned up after transcription
- No permanent storage of voice data
- HTTPS recommended for production

## 📈 Performance

### Optimization Tips
- Use good quality microphone
- Speak clearly and at normal pace
- Minimize background noise
- Ensure stable internet connection

### Supported Audio Formats
- WebM (preferred)
- WAV
- MP3
- OGG
- M4A
- FLAC

## 🚀 Production Deployment

### Backend
1. Set up proper environment variables
2. Use production WSGI server (Gunicorn)
3. Configure HTTPS
4. Set up proper logging

### Frontend
1. Update API_BASE_URL to production server
2. Enable HTTPS
3. Optimize for mobile devices

## 📞 Support

For issues with:
- **Dwani AI**: Contact Dwani AI support
- **Integration**: Check logs and documentation
- **Browser Issues**: Update to latest browser version

---

**Powered by Dwani AI** - Advanced multilingual speech recognition technology
