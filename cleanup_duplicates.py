#!/usr/bin/env python3
"""
Script to clean up duplicate patients in the database
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend-api'))

from app import create_app
from models import db, User, Patient, Record

def cleanup_duplicates():
    """Remove duplicate patients from the database"""
    
    app = create_app()
    
    with app.app_context():
        print("🧹 Cleaning up duplicate patients...")
        print("=" * 50)
        
        # Get all patients
        patients = Patient.query.all()
        
        print(f"📊 Found {len(patients)} total patients")
        
        # Group patients by name
        patient_groups = {}
        for patient in patients:
            # Handle patients with missing names
            if not patient.first_name or not patient.last_name:
                key = f"UNNAMED_{patient.id}"
            else:
                key = f"{patient.first_name.strip()} {patient.last_name.strip()}"
            
            if key not in patient_groups:
                patient_groups[key] = []
            patient_groups[key].append(patient)
        
        print(f"📋 Found {len(patient_groups)} unique patient names")
        print()
        
        duplicates_found = 0
        patients_deleted = 0
        
        for name, patient_list in patient_groups.items():
            if len(patient_list) > 1:
                duplicates_found += 1
                print(f"🔍 Found {len(patient_list)} duplicates for: {name}")
                
                # Sort by ID to keep the first one (or by records count)
                patient_list.sort(key=lambda p: (
                    -len(Record.query.filter_by(patient_id=p.id).all()),  # More records first
                    p.id  # Then by ID
                ))
                
                # Keep the first one (most records or lowest ID)
                keep_patient = patient_list[0]
                records_count = len(Record.query.filter_by(patient_id=keep_patient.id).all())
                
                print(f"   ✅ Keeping: ID {keep_patient.id} (has {records_count} records)")
                
                # Delete the duplicates
                for patient in patient_list[1:]:
                    duplicate_records = Record.query.filter_by(patient_id=patient.id).all()
                    user = User.query.get(patient.user_id)
                    
                    print(f"   ❌ Deleting: ID {patient.id} (has {len(duplicate_records)} records)")
                    
                    # Delete associated records first
                    for record in duplicate_records:
                        db.session.delete(record)
                    
                    # Delete the patient
                    db.session.delete(patient)
                    
                    # Delete the associated user if it exists
                    if user:
                        db.session.delete(user)
                    
                    patients_deleted += 1
                
                print()
        
        # Handle unnamed patients
        unnamed_patients = [p for p in patients if not p.first_name or not p.last_name]
        if unnamed_patients:
            print(f"🔍 Found {len(unnamed_patients)} patients with missing names:")
            for patient in unnamed_patients:
                user = User.query.get(patient.user_id) if patient.user_id else None
                records_count = len(Record.query.filter_by(patient_id=patient.id).all())
                
                print(f"   - ID {patient.id}: '{patient.first_name or 'None'}' '{patient.last_name or 'None'}' "
                      f"(Email: {user.email if user else 'None'}, Records: {records_count})")
                
                # Delete unnamed patients with no records
                if records_count == 0:
                    print(f"     ❌ Deleting unnamed patient with no records")
                    if user:
                        db.session.delete(user)
                    db.session.delete(patient)
                    patients_deleted += 1
            print()
        
        if patients_deleted > 0:
            try:
                db.session.commit()
                print(f"✅ Successfully deleted {patients_deleted} duplicate/invalid patients")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error deleting patients: {str(e)}")
                return
        else:
            print("✅ No duplicates found - database is clean!")
        
        # Show final count
        remaining_patients = Patient.query.all()
        print(f"📊 Final count: {len(remaining_patients)} patients remaining")
        
        print("\n📋 Remaining patients:")
        for patient in remaining_patients:
            records_count = len(Record.query.filter_by(patient_id=patient.id).all())
            print(f"   - {patient.first_name} {patient.last_name} ({records_count} records)")
        
        print("\n🎉 Database cleanup complete!")

if __name__ == "__main__":
    cleanup_duplicates()
