#!/usr/bin/env python3
"""
Script to check what patients are currently in the database
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend-api'))

from app import create_app
from models import db, User, Patient, Record

def check_patients():
    """Check what patients are in the database"""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking patients in database...")
        print("=" * 50)
        
        # Get all patients
        patients = Patient.query.all()
        
        if not patients:
            print("❌ No patients found in database!")
            print("💡 Run 'python populate_test_patients.py' to add test patients")
            return
        
        print(f"📊 Found {len(patients)} patients in database:")
        print()
        
        for i, patient in enumerate(patients, 1):
            # Get user info
            user = User.query.get(patient.user_id)
            
            # Get records count
            records_count = Record.query.filter_by(patient_id=patient.id).count()
            
            print(f"{i}. {patient.first_name} {patient.last_name}")
            print(f"   📧 Email: {user.email if user else 'N/A'}")
            print(f"   📱 Phone: {patient.phone}")
            print(f"   🎂 DOB: {patient.date_of_birth}")
            print(f"   👤 Gender: {patient.gender}")
            print(f"   📄 Records: {records_count}")
            
            # Show records
            if records_count > 0:
                records = Record.query.filter_by(patient_id=patient.id).all()
                for record in records:
                    print(f"      - {record.file_type}: {record.file_name}")
            print()
        
        print("✅ Database check complete!")
        print()
        print("🧪 Test these names in voice search:")
        for patient in patients:
            print(f"   - {patient.first_name} {patient.last_name}")

if __name__ == "__main__":
    check_patients()
