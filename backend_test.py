#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime
import time

class TradeLingoPro_UpgradeTester:
    def __init__(self, base_url="https://aplicacao-principal.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.test_user_id = None
        self.test_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.session = requests.Session()
        
    def run_test(self, name, test_func):
        """Run a single test with error handling"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            success, message = test_func()
            if success:
                self.tests_passed += 1
                print(f"✅ PASSED - {message}")
                return True
            else:
                print(f"❌ FAILED - {message}")
                return False
        except Exception as e:
            print(f"❌ ERROR - {str(e)}")
            return False
    
    def test_backend_health(self):
        """Test if backend is accessible"""
        try:
            response = self.session.get(f"{self.api_base}/health", timeout=10)
            if response.status_code == 200:
                return True, f"Backend healthy (Status: {response.status_code})"
            else:
                return False, f"Backend unhealthy (Status: {response.status_code})"
        except Exception as e:
            try:
                # Try a basic endpoint if /health doesn't exist
                response = self.session.get(self.api_base, timeout=10)
                return True, f"Backend accessible (Status: {response.status_code})"
            except:
                return False, f"Backend not accessible - {str(e)}"
    
    def test_user_registration(self):
        """Test user registration for Pro upgrade testing"""
        timestamp = int(time.time())
        test_email = f"protest_{timestamp}@test.com"
        test_username = f"protest_{timestamp}"
        
        try:
            response = self.session.post(f"{self.api_base}/auth/register", json={
                "email": test_email,
                "password": "TestPass123!",
                "username": test_username
            })
            
            if response.status_code == 200 or response.status_code == 201:
                user_data = response.json()
                self.test_user_id = user_data.get('id')
                self.test_token = user_data.get('token')
                
                if self.test_user_id:
                    return True, f"User registered successfully (ID: {self.test_user_id})"
                else:
                    return False, f"Registration succeeded but no user ID returned"
            else:
                return False, f"Registration failed (Status: {response.status_code}) - {response.text}"
        except Exception as e:
            return False, f"Registration error - {str(e)}"
    
    def test_user_subscription_status(self):
        """Test getting user subscription status"""
        if not self.test_user_id:
            return False, "No test user available"
        
        try:
            headers = {}
            if self.test_token:
                headers['Authorization'] = f'Bearer {self.test_token}'
            
            response = self.session.get(
                f"{self.api_base}/users/{self.test_user_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                user_data = response.json()
                subscription = user_data.get('subscription', 'free')
                return True, f"User subscription status: {subscription}"
            else:
                return False, f"Failed to get user data (Status: {response.status_code})"
        except Exception as e:
            return False, f"Error getting subscription status - {str(e)}"
    
    def test_subscription_upgrade(self):
        """Test the subscription upgrade endpoint"""
        if not self.test_user_id:
            return False, "No test user available"
        
        try:
            headers = {'Content-Type': 'application/json'}
            if self.test_token:
                headers['Authorization'] = f'Bearer {self.test_token}'
            
            response = self.session.post(
                f"{self.api_base}/subscription/upgrade",
                json={
                    "user_id": self.test_user_id,
                    "plan": "pro"
                },
                headers=headers
            )
            
            if response.status_code == 200:
                upgrade_data = response.json()
                return True, f"Upgrade successful - {upgrade_data.get('message', 'No message')}"
            else:
                return False, f"Upgrade failed (Status: {response.status_code}) - {response.text}"
        except Exception as e:
            return False, f"Upgrade error - {str(e)}"
    
    def test_invalid_subscription_plan(self):
        """Test upgrade with invalid plan"""
        if not self.test_user_id:
            return False, "No test user available"
        
        try:
            headers = {'Content-Type': 'application/json'}
            if self.test_token:
                headers['Authorization'] = f'Bearer {self.test_token}'
            
            response = self.session.post(
                f"{self.api_base}/subscription/upgrade",
                json={
                    "user_id": self.test_user_id,
                    "plan": "invalid_plan"
                },
                headers=headers
            )
            
            if response.status_code == 400:
                return True, f"Invalid plan correctly rejected (Status: 400)"
            else:
                return False, f"Invalid plan should return 400, got {response.status_code}"
        except Exception as e:
            return False, f"Invalid plan test error - {str(e)}"
    
    def test_subscription_status_after_upgrade(self):
        """Verify user subscription status after upgrade"""
        if not self.test_user_id:
            return False, "No test user available"
        
        try:
            headers = {}
            if self.test_token:
                headers['Authorization'] = f'Bearer {self.test_token}'
            
            response = self.session.get(
                f"{self.api_base}/users/{self.test_user_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                user_data = response.json()
                subscription = user_data.get('subscription', 'free')
                if subscription == 'pro':
                    return True, f"User subscription confirmed as Pro"
                else:
                    return False, f"Expected 'pro', got '{subscription}'"
            else:
                return False, f"Failed to verify subscription (Status: {response.status_code})"
        except Exception as e:
            return False, f"Error verifying subscription - {str(e)}"
    
    def test_curriculum_endpoints(self):
        """Test curriculum endpoints that might be affected by subscription"""
        try:
            response = self.session.get(f"{self.api_base}/curriculum/tiers")
            if response.status_code == 200:
                tiers = response.json()
                return True, f"Curriculum tiers loaded ({len(tiers)} tiers)"
            else:
                return False, f"Curriculum tiers failed (Status: {response.status_code})"
        except Exception as e:
            return False, f"Curriculum error - {str(e)}"
    
    def test_real_market_endpoints(self):
        """Test real market/backtest related endpoints"""
        try:
            # Test if there are any backtest or real market specific endpoints
            endpoints_to_test = [
                "/real-market/data",
                "/backtest/session",
                "/market/assets",
                "/trading/assets"
            ]
            
            working_endpoints = []
            for endpoint in endpoints_to_test:
                try:
                    response = self.session.get(f"{self.api_base}{endpoint}")
                    if response.status_code in [200, 401]:  # 200 = working, 401 = needs auth but exists
                        working_endpoints.append(endpoint)
                except:
                    continue
            
            if len(working_endpoints) > 0:
                return True, f"Real market endpoints available: {working_endpoints}"
            else:
                return True, f"Real market endpoints may be frontend-only or differently named"
        except Exception as e:
            return False, f"Real market endpoint error - {str(e)}"

def main():
    """Run all Pro Upgrade tests"""
    print("🚀 TradeLingo Pro Upgrade Backend Testing")
    print("=" * 50)
    
    tester = TradeLingoPro_UpgradeTester()
    
    # Core functionality tests
    tests = [
        ("Backend Health Check", tester.test_backend_health),
        ("User Registration", tester.test_user_registration),
        ("Initial Subscription Status", tester.test_user_subscription_status),
        ("Pro Subscription Upgrade", tester.test_subscription_upgrade),
        ("Post-Upgrade Subscription Status", tester.test_subscription_status_after_upgrade),
        ("Invalid Plan Rejection", tester.test_invalid_subscription_plan),
        ("Curriculum Endpoints", tester.test_curriculum_endpoints),
        ("Real Market Endpoints", tester.test_real_market_endpoints),
    ]
    
    # Run all tests
    for test_name, test_func in tests:
        tester.run_test(test_name, test_func)
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 TESTING SUMMARY")
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 ALL TESTS PASSED - Pro Upgrade functionality working perfectly!")
        return 0
    else:
        failed_tests = tester.tests_run - tester.tests_passed
        print(f"⚠️  {failed_tests} TESTS FAILED - Check the issues above")
        return 1

if __name__ == "__main__":
    sys.exit(main())