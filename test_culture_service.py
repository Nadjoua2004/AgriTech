#!/usr/bin/env python3
"""
Simple test script for culture service
"""
import requests
import json

def test_service():
    base_url = "https://cultures-service.onrender.com"
    
    print("Testing Culture Service...")
    print(f"Base URL: {base_url}")
    
    # Test health endpoint
    try:
        print("\n1. Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.Timeout:
        print("❌ Health endpoint timed out")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test public endpoint
    try:
        print("\n2. Testing public endpoint...")
        response = requests.get(f"{base_url}/api/cultures/public", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.Timeout:
        print("❌ Public endpoint timed out")
    except Exception as e:
        print(f"❌ Public endpoint error: {e}")
    
    # Test main endpoint (should fail with auth)
    try:
        print("\n3. Testing main endpoint (no auth)...")
        response = requests.get(f"{base_url}/api/cultures", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.Timeout:
        print("❌ Main endpoint timed out")
    except Exception as e:
        print(f"❌ Main endpoint error: {e}")

if __name__ == "__main__":
    test_service()
