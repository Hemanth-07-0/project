#!/usr/bin/env python3
"""
Test script to verify the improved name matching functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend-api'))

from backend_api.routes.voice import search_patient_records_by_name, calculate_name_match_confidence

def test_name_matching():
    """Test the name matching logic with various scenarios"""
    
    print("🧪 Testing Name Matching Logic")
    print("=" * 50)
    
    # Test cases that should work correctly
    test_cases = [
        # (search_text, expected_behavior)
        ("john doe", "Should match 'John Doe' exactly"),
        ("John Doe", "Should match 'john doe' (case insensitive)"),
        ("jane smith", "Should NOT match 'John Doe'"),
        ("john", "Should match 'John Doe' partially but with lower confidence"),
        ("doe", "Should match 'John Doe' by last name"),
        ("johnny doe", "Should match 'John Doe' with partial first name"),
        ("john d", "Should match 'John Doe' with partial last name"),
        ("j doe", "Should NOT match 'John Doe' (too short first name)"),
        ("", "Should return no matches"),
        ("xyz abc", "Should return no matches for non-existent name"),
    ]
    
    print("\n📊 Confidence Score Tests:")
    print("-" * 30)
    
    for search_text, expected in test_cases:
        confidence = calculate_name_match_confidence(search_text.lower(), "john doe")
        print(f"'{search_text}' vs 'John Doe': {confidence}% - {expected}")
    
    print("\n🎯 Edge Cases:")
    print("-" * 20)
    
    edge_cases = [
        ("john johnson", "john doe"),  # Similar first name
        ("jane doe", "john doe"),      # Same last name
        ("jon doe", "john doe"),       # Typo in first name
        ("john do", "john doe"),       # Typo in last name
        ("johndoe", "john doe"),       # No space
        ("john  doe", "john doe"),     # Extra spaces
    ]
    
    for search, target in edge_cases:
        confidence = calculate_name_match_confidence(search.lower(), target.lower())
        print(f"'{search}' vs '{target}': {confidence}%")
    
    print("\n✅ Test completed!")
    print("\nExpected behavior:")
    print("- Exact matches should score 100%")
    print("- Good partial matches should score 70-95%")
    print("- Poor matches should score <60%")
    print("- Non-matches should score 0%")

if __name__ == "__main__":
    test_name_matching()
