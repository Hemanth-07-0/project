#!/usr/bin/env python3
"""
Script to test the voice search functionality directly
"""

import sys
import os
import requests
import json

def test_voice_search():
    """Test the voice search API directly"""
    
    print("🧪 Testing Voice Search API")
    print("=" * 40)
    
    # Backend URL
    base_url = "http://localhost:5000"
    
    # Test cases
    test_cases = [
        "John Doe",
        "Jane Smith", 
        "Michael Johnson",
        "Sarah Williams",
        "David Brown",
        "NonExistent Patient"
    ]
    
    print(f"🔗 Testing against: {base_url}")
    print()
    
    for test_name in test_cases:
        print(f"🔍 Testing: '{test_name}'")
        
        try:
            # Test the search-by-text endpoint
            response = requests.post(
                f"{base_url}/voice/search-by-text",
                json={"search_text": test_name},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success') and data.get('matching_records'):
                    records = data['matching_records']
                    print(f"   ✅ Found {len(records)} matching record(s)")
                    
                    for i, record in enumerate(records, 1):
                        patient_name = record.get('patient_name', 'Unknown')
                        confidence = record.get('match_confidence', 0)
                        record_count = len(record.get('records', []))
                        
                        print(f"      {i}. {patient_name} (Confidence: {confidence}%, Records: {record_count})")
                        
                        # Show first few records
                        for j, file_record in enumerate(record.get('records', [])[:2]):
                            file_type = file_record.get('file_type', 'Unknown')
                            file_name = file_record.get('file_name', 'Unknown')
                            print(f"         - {file_type}: {file_name}")
                        
                        if len(record.get('records', [])) > 2:
                            print(f"         ... and {len(record.get('records', [])) - 2} more")
                
                else:
                    print(f"   ❌ No records found")
                    
            else:
                print(f"   ❌ API Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"      Error: {error_data.get('error', 'Unknown error')}")
                except:
                    print(f"      Error: {response.text}")
                    
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection Error: Backend not running at {base_url}")
            print(f"      💡 Start backend with: python start_backend.py")
            break
            
        except requests.exceptions.Timeout:
            print(f"   ❌ Timeout: Request took too long")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        print()
    
    print("🎯 Test Summary:")
    print("- If you see ✅ results, the voice search is working correctly")
    print("- If you see ❌ errors, check that the backend is running")
    print("- Names should return consistent results (no random patients)")
    print()
    print("🚀 Next Steps:")
    print("1. Start backend: python start_backend.py")
    print("2. Open browser: 2nd/index.html")
    print("3. Use 'Test Database Search' section")
    print("4. Try the names that showed ✅ results above")

if __name__ == "__main__":
    test_voice_search()
