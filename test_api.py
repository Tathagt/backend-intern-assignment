"""
API Testing Examples
Run with: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_organization():
    """Test creating a new organization"""
    print("\n1. Testing Organization Creation...")
    
    data = {
        "organization_name": "test_corp",
        "email": "admin@testcorp.com",
        "password": "securepass123"
    }
    
    response = requests.post(f"{BASE_URL}/org/create", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def test_admin_login(email, password):
    """Test admin login"""
    print("\n2. Testing Admin Login...")
    
    data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/admin/login", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json().get("access_token")

def test_get_organization(org_name):
    """Test getting organization details"""
    print("\n3. Testing Get Organization...")
    
    response = requests.get(f"{BASE_URL}/org/get", params={"organization_name": org_name})
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_update_organization(org_name, token):
    """Test updating organization"""
    print("\n4. Testing Update Organization...")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "organization_name": org_name,
        "email": "newemail@testcorp.com"
    }
    
    response = requests.put(f"{BASE_URL}/org/update", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_delete_organization(org_name, token):
    """Test deleting organization"""
    print("\n5. Testing Delete Organization...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.delete(
        f"{BASE_URL}/org/delete",
        params={"organization_name": org_name},
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("=" * 50)
    print("API Testing Suite")
    print("=" * 50)
    
    try:
        # Test flow
        org_data = test_create_organization()
        token = test_admin_login("admin@testcorp.com", "securepass123")
        test_get_organization("test_corp")
        test_update_organization("test_corp", token)
        test_delete_organization("test_corp", token)
        
        print("\n" + "=" * 50)
        print("All tests completed!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure the API server is running on http://localhost:8000")