"""
Example demonstrating LangSafe API usage.

This example shows how to use the LangSafe API to scan input and output prompts
for sensitive information.
"""
import requests
import json
import time


def test_langsafe_api():
    """Test the LangSafe API endpoints."""
    
    # API configuration
    base_url = "http://localhost:8000"
    api_key = "your-api-key-here"
    
    print("🔍 LangSafe API Example")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "name": "Input with email",
            "prompt": "Hello, my email is user@example.com and I need help",
            "user_id": "user123"
        },
        {
            "name": "Input with password",
            "prompt": "My password is secret123 and my username is admin",
            "user_id": "user456"
        },
        {
            "name": "Output with credit card",
            "prompt": "The user's credit card number is 1234-5678-9012-3456",
            "user_id": "user789"
        },
        {
            "name": "Clean input",
            "prompt": "Hello world, how are you today?",
            "user_id": "user999"
        }
    ]
    
    try:
        # Check server health
        print("\n1. Checking server health...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Server status: {health['status']}")
            print(f"📦 Version: {health['version']}")
            if health.get('ngrok_url'):
                print(f"🌐 Ngrok URL: {health['ngrok_url']}")
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return
        
        # Test input scanner
        print("\n2. Testing input scanner...")
        for i, test_case in enumerate(test_cases[:2], 1):
            print(f"\n   Test {i}: {test_case['name']}")
            
            payload = {
                "api_key": api_key,
                "prompt": test_case["prompt"],
                "user_id": test_case["user_id"]
            }
            
            response = requests.post(
                f"{base_url}/api/input-scanner",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success: {result['success']}")
                print(f"   📝 Processed: {result['prompt']}")
                print(f"   💬 Message: {result['message']}")
                
                if result.get('metadata', {}).get('sensitive_patterns_found'):
                    print(f"   ⚠️  Sensitive patterns found: {result['metadata']['sensitive_patterns_found']}")
            else:
                print(f"   ❌ Error: {response.status_code} - {response.text}")
        
        # Test output scanner
        print("\n3. Testing output scanner...")
        for i, test_case in enumerate(test_cases[2:], 1):
            print(f"\n   Test {i}: {test_case['name']}")
            
            payload = {
                "api_key": api_key,
                "prompt": test_case["prompt"],
                "user_id": test_case["user_id"]
            }
            
            response = requests.post(
                f"{base_url}/api/output-scanner",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success: {result['success']}")
                print(f"   📝 Processed: {result['prompt']}")
                print(f"   💬 Message: {result['message']}")
                
                if result.get('metadata', {}).get('sensitive_patterns_found'):
                    print(f"   ⚠️  Sensitive patterns found: {result['metadata']['sensitive_patterns_found']}")
            else:
                print(f"   ❌ Error: {response.status_code} - {response.text}")
        
        # Get ngrok info
        print("\n4. Getting ngrok information...")
        response = requests.get(f"{base_url}/api/ngrok-info")
        if response.status_code == 200:
            ngrok_info = response.json()
            print(f"   🔄 Ngrok running: {ngrok_info['is_running']}")
            print(f"   🔌 Port: {ngrok_info['port']}")
            print(f"   📦 Ngrok installed: {ngrok_info['ngrok_installed']}")
            if ngrok_info.get('public_url'):
                print(f"   🌐 Public URL: {ngrok_info['public_url']}")
        else:
            print(f"   ❌ Failed to get ngrok info: {response.status_code}")
        
        print("\n🎉 All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server.")
        print("💡 Make sure the LangSafe server is running:")
        print("   python -m src.langsafe.main")
    except Exception as e:
        print(f"❌ Error: {e}")


def interactive_test():
    """Interactive test mode."""
    
    base_url = "http://localhost:8000"
    api_key = "your-api-key-here"
    
    print("\n🔍 Interactive LangSafe Test")
    print("=" * 40)
    print("Enter 'quit' to exit")
    print()
    
    while True:
        try:
            # Get user input
            prompt = input("Enter a prompt to scan: ").strip()
            
            if prompt.lower() == 'quit':
                break
            
            if not prompt:
                print("Please enter a valid prompt.")
                continue
            
            # Choose scanner type
            scanner_type = input("Scanner type (input/output): ").strip().lower()
            
            if scanner_type not in ['input', 'output']:
                print("Please choose 'input' or 'output'.")
                continue
            
            # Get user ID
            user_id = input("User ID: ").strip() or "test-user"
            
            # Make API request
            endpoint = f"/api/{scanner_type}-scanner"
            payload = {
                "api_key": api_key,
                "prompt": prompt,
                "user_id": user_id
            }
            
            response = requests.post(f"{base_url}{endpoint}", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n✅ Success: {result['success']}")
                print(f"📝 Processed: {result['prompt']}")
                print(f"💬 Message: {result['message']}")
                
                if result.get('metadata'):
                    metadata = result['metadata']
                    print(f"📊 Metadata:")
                    print(f"   - User ID: {metadata.get('user_id')}")
                    print(f"   - Scan Type: {metadata.get('scan_type')}")
                    print(f"   - Timestamp: {metadata.get('timestamp')}")
                    
                    if metadata.get('sensitive_patterns_found'):
                        print(f"   - Sensitive patterns: {metadata['sensitive_patterns_found']}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    # Run automated tests
    test_langsafe_api()
    
    # Run interactive test
    print("\n" + "="*50)
    interactive_test() 