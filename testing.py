#!/usr/bin/env python3
"""
Test both model servers directly
Run this in PowerShell or Command Prompt
"""

import requests
import json
import time

# Configuration
MODEL1 = {
    "name": "Dictatorai (1-to-1)",
    "url": "http://85.218.235.6:33100"
}

MODEL2 = {
    "name": "Mistral (Speechmodel)",
    "url": "http://189.132.2.88:17075"
}

def test_model(model):
    """Test a single model"""
    print(f"\n{'='*60}")
    print(f"Testing: {model['name']}")
    print(f"URL: {model['url']}")
    print(f"{'='*60}")
    
    # Test 1: Health Check
    print("\n[1] Health Check...")
    try:
        response = requests.get(f"{model['url']}/health", timeout=10)
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Response: {response.json()}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    # Test 2: Models Endpoint
    print("\n[2] Models Endpoint...")
    try:
        response = requests.get(f"{model['url']}/v1/models", timeout=10)
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Response: {response.json()}")
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    # Test 3: Chat Completion
    print("\n[3] Chat Completion Test...")
    payload = {
        "model": "default",
        "messages": [
            {
                "role": "user",
                "content": "Say hello briefly in one sentence"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100,
        "stream": False
    }
    
    print(f"Sending payload: {json.dumps(payload, indent=2)}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{model['url']}/v1/chat/completions",
            json=payload,
            timeout=120,
            headers={"Content-Type": "application/json"}
        )
        elapsed = time.time() - start_time
        
        print(f"\n✓ Status: {response.status_code}")
        print(f"✓ Response Time: {elapsed:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Full Response: {json.dumps(result, indent=2)}")
            
            try:
                reply = result['choices'][0]['message']['content']
                print(f"\n✓✓✓ MODEL WORKING!")
                print(f"Reply: {reply}")
                return True
            except KeyError as e:
                print(f"✗ Could not extract reply: {e}")
                print(f"Response structure: {list(result.keys())}")
                return False
        else:
            print(f"✗ Error Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"✗ Request timed out (server might be processing)")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("MODEL SERVER TEST SUITE")
    print("="*60)
    
    results = {}
    
    # Test both models
    results[MODEL1['name']] = test_model(MODEL1)
    time.sleep(2)
    results[MODEL2['name']] = test_model(MODEL2)
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    for model_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{model_name}: {status}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()