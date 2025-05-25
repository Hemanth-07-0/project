#!/usr/bin/env python3
"""
Test data setup script for Dwani AI voice recognition integration
This script adds sample patient data to test the voice-based record lookup functionality
"""

import sys
import os
from datetime import datetime

# Add backend-api to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend-api'))

try:
    from app import create_app
    from models import db, User, Patient, Record
    
    def setup_test_data():
        """Setup test patient data for voice recognition testing"""
        app = create_app()
        
        with app.app_context():
            print("Setting up test data for voice recognition...")
            
            # Sample patients to add
            test_patients = [
                {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john.doe@example.com',
                    'records': [
                        {'file_name': 'Blood_Test_Results.pdf', 'file_type': 'Lab Report', 'notes': 'Annual blood work'},
                        {'file_name': 'X_Ray_Report.pdf', 'file_type': 'Radiology', 'notes': 'Chest X-ray'},
                        {'file_name': 'Prescription_History.pdf', 'file_type': 'Prescription', 'notes': 'Current medications'}
                    ]
                },
                {
                    'first_name': 'Jane',
                    'last_name': 'Smith',
                    'email': 'jane.smith@example.com',
                    'records': [
                        {'file_name': 'Annual_Checkup.pdf', 'file_type': 'Consultation Notes', 'notes': 'Routine physical exam'},
                        {'file_name': 'Vaccination_Record.pdf', 'file_type': 'Immunization', 'notes': 'COVID-19 vaccination'}
                    ]
                },
                {
                    'first_name': 'Michael',
                    'last_name': 'Johnson',
                    'email': 'michael.johnson@example.com',
                    'records': [
                        {'file_name': 'MRI_Scan_Report.pdf', 'file_type': 'Radiology', 'notes': 'Brain MRI scan'},
                        {'file_name': 'Cardiology_Report.pdf', 'file_type': 'Specialist Report', 'notes': 'Heart examination'}
                    ]
                },
                {
                    'first_name': 'Sarah',
                    'last_name': 'Williams',
                    'email': 'sarah.williams@example.com',
                    'records': [
                        {'file_name': 'Diabetes_Management.pdf', 'file_type': 'Treatment Plan', 'notes': 'Diabetes care plan'},
                        {'file_name': 'Lab_Results_Glucose.pdf', 'file_type': 'Lab Report', 'notes': 'Blood glucose monitoring'}
                    ]
                }
            ]
            
            for patient_data in test_patients:
                # Check if patient already exists
                existing_patient = Patient.query.join(User).filter(
                    User.email == patient_data['email']
                ).first()
                
                if existing_patient:
                    print(f"Patient {patient_data['first_name']} {patient_data['last_name']} already exists, skipping...")
                    continue
                
                # Create user
                user = User(
                    email=patient_data['email'],
                    user_type='patient'
                )
                user.set_password('password123')  # Default password for testing
                db.session.add(user)
                db.session.flush()  # Get the user ID
                
                # Create patient
                patient = Patient(
                    user_id=user.id,
                    first_name=patient_data['first_name'],
                    last_name=patient_data['last_name'],
                    date_of_birth='1990-01-01',
                    gender='Unknown',
                    phone='555-0123',
                    address='123 Test Street',
                    city='Test City',
                    state='Test State',
                    zip_code='12345'
                )
                db.session.add(patient)
                db.session.flush()  # Get the patient ID
                
                # Create sample records
                for record_data in patient_data['records']:
                    # Create dummy file data (small PDF-like content)
                    dummy_file_content = f"Sample medical record for {patient_data['first_name']} {patient_data['last_name']}\nFile: {record_data['file_name']}\nType: {record_data['file_type']}\nNotes: {record_data['notes']}\nGenerated: {datetime.now()}"
                    
                    record = Record(
                        patient_id=patient.id,
                        file_name=record_data['file_name'],
                        file_type=record_data['file_type'],
                        file_size='1.2 MB',
                        file_data=dummy_file_content.encode('utf-8'),
                        notes=record_data['notes']
                    )
                    db.session.add(record)
                
                print(f"✅ Added patient: {patient_data['first_name']} {patient_data['last_name']} with {len(patient_data['records'])} records")
            
            # Commit all changes
            db.session.commit()
            print("\n🎉 Test data setup completed successfully!")
            print("\nYou can now test voice recognition with these patient names:")
            for patient_data in test_patients:
                print(f"  - {patient_data['first_name']} {patient_data['last_name']}")
            
            print("\nTo test:")
            print("1. Start the backend server: python backend-api/run.py")
            print("2. Open public/patient-health-records.html in your browser")
            print("3. Click START RECORDING and speak one of the patient names above")
            print("4. The system should display matching medical records")
    
    if __name__ == '__main__':
        setup_test_data()
        
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure you're running this from the project root directory")
    print("and that the backend dependencies are installed")
except Exception as e:
    print(f"❌ Error setting up test data: {e}")
    import traceback
    traceback.print_exc()
