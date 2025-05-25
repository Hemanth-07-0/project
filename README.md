# Visbo Healthcare Platform

A healthcare platform with patient records management and voice authentication.

## Project Structure

- `backend-api/`: Backend server (Flask)
- `public/`: Frontend files (HTML, CSS, JavaScript)

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend-api
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Initialize the database:
   ```
   python init_db.py
   ```

6. Run the server:
   ```
   python run.py
   ```

The backend API will be available at http://localhost:5000

### Frontend Setup

The frontend is static HTML/CSS/JavaScript and doesn't require any build steps.

1. Serve the `public` directory using any static file server.

2. For development, you can use Python's built-in HTTP server:
   ```
   cd public
   python -m http.server 8000
   ```

The frontend will be available at http://localhost:8000

## Key Features

1. **Unified Login System**
   - Tabbed interface for patient and doctor/hospital login
   - Distinct visual styling for each user type

2. **Voice Authentication**
   - Patients can use voice recognition for enhanced security
   - Voice patterns are stored and verified against hospital records

3. **Patient Records Management**
   - Upload and manage medical records
   - View and download records
   - Secure access to patient information

4. **Responsive Design**
   - Works seamlessly on desktop and mobile devices
   - Intuitive layout adapts to different screen sizes

## API Endpoints

### Authentication

- `POST /auth/signup/<user_type>`: Register a new user (patient or hospital)
- `POST /auth/login`: Login and get JWT token
- `GET /auth/profile`: Get current user profile
- `PUT /auth/profile`: Update user profile

### Records

- `GET /records/list`: List all records
- `GET /records/patient/<patient_id>`: Get records for a specific patient
- `GET /records/<record_id>`: Get a specific record
- `POST /records/add`: Add a new record (JSON)
- `POST /records/upload`: Upload a record file
- `GET /records/download/<record_id>`: Download a record file
- `DELETE /records/delete/<record_id>`: Delete a record

## Database Schema

The application uses SQLite with the following tables:

- `users`: Authentication information
- `patients`: Patient profiles
- `hospitals`: Hospital profiles
- `records`: Medical records
- `voice_auth`: Voice authentication data

## User Flow

1. Users navigate to the login page from the homepage
2. They select either "Patient" or "Doctor/Hospital" tab
3. They enter their credentials and submit the form
4. Upon successful authentication, they are redirected to the appropriate dashboard
5. Patients can view their records and upload voice samples
6. Hospitals can manage patient records and view analytics

## Voice Authentication Process

1. Patient records their voice by saying their full name
2. The system extracts the name from the voice recording
3. The name is compared against hospital records
4. If verified, the voice file is uploaded to the patient's profile
5. The patient can then use voice authentication for future logins

## Future Enhancements

- Two-factor authentication for enhanced security
- Integration with hospital electronic health record systems
- Biometric authentication options (fingerprint, facial recognition)
- Accessibility improvements for users with disabilities