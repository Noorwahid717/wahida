#!/usr/bin/env python3
"""Test Supabase connection and diagnose CORS issues."""

import os
import sys
import requests
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "apps" / "api"))

def test_supabase_connection():
    """Test basic Supabase connectivity."""

    print("🔍 Testing Supabase Connection")
    print("=" * 50)

    # Load environment variables
    supabase_url = "https://gyyiuhgcbggxzozasfji.supabase.co"
    supabase_anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd5eWl1aGdjYmdneHpvemFzZmppIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkwNTk5NjIsImV4cCI6MjA3NDYzNTk2Mn0.vumFtnaPhkZEosWAPlK01OHYWe-C_mAUhV_b6N0lMLE"

    print(f"📍 Supabase URL: {supabase_url}")
    print(f"🔑 API Key: {supabase_anon_key[:20]}...")

    # Test 1: Basic connectivity
    print("\n1️⃣ Testing basic connectivity...")
    try:
        response = requests.get(f"{supabase_url}/rest/v1/", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Basic connection successful")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")

    # Test 2: Auth endpoint
    print("\n2️⃣ Testing auth endpoint...")
    try:
        headers = {
            "apikey": supabase_anon_key,
            "Content-Type": "application/json"
        }
        response = requests.get(f"{supabase_url}/auth/v1/user", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 401]:  # 401 is expected without auth
            print("   ✅ Auth endpoint accessible")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Auth endpoint failed: {e}")

    # Test 3: CORS headers check
    print("\n3️⃣ Testing CORS headers...")
    try:
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,authorization"
        }
        response = requests.options(f"{supabase_url}/auth/v1/signup",
                                  headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")

        # Check CORS headers
        cors_headers = {
            'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
            'access-control-allow-methods': response.headers.get('access-control-allow-methods'),
            'access-control-allow-headers': response.headers.get('access-control-allow-headers')
        }

        print("   CORS Headers:")
        for header, value in cors_headers.items():
            if value:
                print(f"     ✅ {header}: {value}")
            else:
                print(f"     ❌ {header}: Missing")

        if cors_headers['access-control-allow-origin']:
            print("   ✅ CORS configured")
        else:
            print("   ❌ CORS not configured properly")

    except Exception as e:
        print(f"   ❌ CORS test failed: {e}")

    # Test 4: Database connection (if available)
    print("\n4️⃣ Testing database connection...")
    try:
        # This would require database credentials
        print("   ℹ️  Database test requires direct DB credentials")
        print("   🔗 Check Railway/Supabase dashboard for DB status")
    except Exception as e:
        print(f"   ❌ Database test failed: {e}")

    print("\n" + "=" * 50)
    print("🎯 Connection Test Complete")
    print("\n💡 Troubleshooting Tips:")
    print("   • If CORS fails: Update Site URL in Supabase dashboard")
    print("   • If auth fails: Check API keys in environment")
    print("   • If network fails: Check firewall/proxy settings")
    print("   • For frontend: Ensure NEXT_PUBLIC_SUPABASE_URL is set")

if __name__ == "__main__":
    test_supabase_connection()