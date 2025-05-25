#!/usr/bin/env python3
"""
Script to populate the database with test patients for voice search testing
"""

import sys
import os

# Add the backend-api directory to the Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend-api')
sys.path.insert(0, backend_path)

from app import create_app
from models import db, User, Patient, Record
from datetime import datetime

def populate_test_patients():
    """Add test patients to the database"""

    app = create_app()

    with app.app_context():
        print("🏥 Populating database with test patients...")

        # Test patients data
        test_patients = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@patient.com',
                'date_of_birth': '1985-05-15',
                'gender': 'Male',
                'phone': '+91-9876543210',
                'records': [
                    {'file_name': 'blood_test_john.pdf', 'file_type': 'Blood Test', 'notes': 'Annual checkup blood work'},
                    {'file_name': 'xray_john.pdf', 'file_type': 'X-Ray', 'notes': 'Chest X-ray for cough'}
                ]
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane.smith@patient.com',
                'date_of_birth': '1990-08-22',
                'gender': 'Female',
                'phone': '+91-9876543211',
                'records': [
                    {'file_name': 'consultation_jane.pdf', 'file_type': 'Consultation', 'notes': 'General health consultation'},
                    {'file_name': 'lab_report_jane.pdf', 'file_type': 'Lab Report', 'notes': 'Comprehensive metabolic panel'}
                ]
            },
            {
                'first_name': 'Michael',
                'last_name': 'Johnson',
                'email': 'michael.johnson@patient.com',
                'date_of_birth': '1978-12-03',
                'gender': 'Male',
                'phone': '+91-9876543212',
                'records': [
                    {'file_name': 'mri_michael.pdf', 'file_type': 'MRI', 'notes': 'Brain MRI scan'},
                    {'file_name': 'prescription_michael.pdf', 'file_type': 'Prescription', 'notes': 'Medication for headaches'}
                ]
            },
            {
                'first_name': 'Sarah',
                'last_name': 'Williams',
                'email': 'sarah.williams@patient.com',
                'date_of_birth': '1995-03-18',
                'gender': 'Female',
                'phone': '+91-9876543213',
                'records': [
                    {'file_name': 'vaccination_sarah.pdf', 'file_type': 'Vaccination', 'notes': 'COVID-19 vaccination record'},
                    {'file_name': 'checkup_sarah.pdf', 'file_type': 'Checkup', 'notes': 'Annual physical examination'}
                ]
            },
            {
                'first_name': 'David',
                'last_name': 'Brown',
                'email': 'david.brown@patient.com',
                'date_of_birth': '1982-07-09',
                'gender': 'Male',
                'phone': '+91-9876543214',
                'records': [
                    {'file_name': 'ecg_david.pdf', 'file_type': 'ECG', 'notes': 'Electrocardiogram test'},
                    {'file_name': 'blood_pressure_david.pdf', 'file_type': 'Blood Pressure', 'notes': 'Hypertension monitoring'}
                ]
            }
        ]

        created_count = 0

        for patient_data in test_patients:
            # Check if patient already exists
            existing_patient = Patient.query.filter_by(
                first_name=patient_data['first_name'],
                last_name=patient_data['last_name']
            ).first()

            if existing_patient:
                print(f"⚠️  Patient {patient_data['first_name']} {patient_data['last_name']} already exists, skipping...")
                continue

            try:
                # Create user account
                user = User(
                    email=patient_data['email'],
                    user_type='patient'
                )
                user.set_password('patient123')  # Default password
                db.session.add(user)
                db.session.flush()

                # Create patient
                patient = Patient(
                    user_id=user.id,
                    first_name=patient_data['first_name'],
                    last_name=patient_data['last_name'],
                    date_of_birth=patient_data['date_of_birth'],
                    gender=patient_data['gender'],
                    phone=patient_data['phone']
                )
                db.session.add(patient)
                db.session.flush()

                # Create records
                for record_data in patient_data['records']:
                    record = Record(
                        patient_id=patient.id,
                        file_name=record_data['file_name'],
                        file_type=record_data['file_type'],
                        file_size='1.2 MB',  # Default size
                        notes=record_data['notes'],
                        upload_date=datetime.now()
                    )
                    db.session.add(record)

                db.session.commit()
                created_count += 1
                print(f"✅ Created patient: {patient_data['first_name']} {patient_data['last_name']} with {len(patient_data['records'])} records")

            except Exception as e:
                db.session.rollback()
                print(f"❌ Error creating patient {patient_data['first_name']} {patient_data['last_name']}: {str(e)}")

        print(f"\n🎉 Successfully created {created_count} test patients!")
        print("\n📋 Test patients available for voice search:")
        print("- John Doe")
        print("- Jane Smith")
        print("- Michael Johnson")
        print("- Sarah Williams")
        print("- David Brown")
        print("\n💡 You can now test the voice search with these names!")

if __name__ == "__main__":
    populate_test_patients()
