#!/usr/bin/env python3
"""Test the GitHub Issue Analysis endpoint"""
import requests
import json
import time

print("\n" + "="*60)
print("Testing GitHub Issue Analysis Endpoint")
print("="*60)

# Test data
payload = {
    'repo_url': 'https://github.com/facebook/react',
    'issue_number': 1
}

print("\nRequest Details:")
print(f"  Endpoint: http://localhost:8000/analyze")
print(f"  Repository: https://github.com/facebook/react")
print(f"  Issue Number: 1")
print("\nSending request to backend...\n")

try:
    response = requests.post('http://localhost:8000/analyze', json=payload, timeout=60)
    
    if response.status_code == 200:
        result = response.json()
        print("✓ SUCCESS! Analysis Result:")
        print("="*60)
        print(json.dumps(result, indent=2))
        print("="*60)
        
        # Verify all required fields
        required_fields = ['summary', 'type', 'priority_score', 'suggested_labels', 'potential_impact']
        print("\nField Validation:")
        for field in required_fields:
            if field in result:
                print(f"  ✓ {field}: Present")
            else:
                print(f"  ✗ {field}: MISSING")
    else:
        print(f"✗ Error: Status {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
except Exception as e:
    print(f"✗ Error connecting to backend: {e}")
    print("\nMake sure the backend is running with:")
    print("  python backend/main.py")
