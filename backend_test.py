#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class TradeLingoBE_Tester:
    def __init__(self, base_url="https://aplicacao-principal.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details="", expected_status=None, actual_status=None):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
            if expected_status and actual_status:
                print(f"   Expected status: {expected_status}, Got: {actual_status}")
        
        self.test_results.append({
            "test_name": name,
            "success": success,
            "details": details,
            "expected_status": expected_status,
            "actual_status": actual_status
        })

    def test_health_endpoint(self):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test("Health Check", True)
                    return True
                else:
                    self.log_test("Health Check", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}", 200, response.status_code)
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
            return False

    def test_root_endpoint(self):
        """Test root API endpoint"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "TradeLingo API" in data.get("message", ""):
                    self.log_test("Root Endpoint", True)
                    return True
                else:
                    self.log_test("Root Endpoint", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Root Endpoint", False, f"HTTP {response.status_code}", 200, response.status_code)
                return False
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Exception: {str(e)}")
            return False

    def test_specific_user_login(self):
        """Test login with specific test user credentials"""
        try:
            login_data = {
                "email": "rsilva@test.com",
                "password": "Test123456"
            }
            
            response = requests.post(
                f"{self.api_url}/auth/login", 
                json=login_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['id', 'username', 'email', 'xp', 'level', 'subscription', 'rank']
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test("Demo Login", False, f"Missing fields: {missing_fields}")
                    return False
                
                if data.get('email') == 'rsilva@test.com':
                    self.log_test("Specific User Login", True)
                    return data
                else:
                    self.log_test("Specific User Login", False, f"Wrong email returned: {data.get('email')}")
                    return False
            else:
                try:
                    error_data = response.json()
                    self.log_test("Specific User Login", False, f"HTTP {response.status_code}: {error_data}", 200, response.status_code)
                except:
                    self.log_test("Specific User Login", False, f"HTTP {response.status_code}: {response.text}", 200, response.status_code)
                return False
                
        except Exception as e:
            self.log_test("Specific User Login", False, f"Exception: {str(e)}")
            return False

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        try:
            login_data = {
                "email": "invalid@test.com",
                "password": "wrongpassword"
            }
            
            response = requests.post(
                f"{self.api_url}/auth/login", 
                json=login_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 401:
                self.log_test("Invalid Login (401 Expected)", True)
                return True
            else:
                self.log_test("Invalid Login (401 Expected)", False, f"Expected 401, got {response.status_code}", 401, response.status_code)
                return False
                
        except Exception as e:
            self.log_test("Invalid Login (401 Expected)", False, f"Exception: {str(e)}")
            return False

    def test_lessons_endpoint(self, user_data=None):
        """Test lessons endpoint"""
        try:
            url = f"{self.api_url}/lessons"
            if user_data:
                url += f"?user_id={user_data['id']}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    # Check if lessons have required fields
                    lesson = data[0]
                    required_fields = ['id', 'level', 'title', 'description', 'xp_reward']
                    missing_fields = [field for field in required_fields if field not in lesson]
                    
                    if missing_fields:
                        self.log_test("Lessons Endpoint", False, f"Missing fields in lesson: {missing_fields}")
                        return False
                    
                    self.log_test("Lessons Endpoint", True)
                    return True
                else:
                    self.log_test("Lessons Endpoint", False, "No lessons returned or invalid format")
                    return False
            else:
                self.log_test("Lessons Endpoint", False, f"HTTP {response.status_code}", 200, response.status_code)
                return False
                
        except Exception as e:
            self.log_test("Lessons Endpoint", False, f"Exception: {str(e)}")
            return False

    def test_category_lesson(self, user_data=None):
        """Test category lesson endpoint (for book functionality)"""
        try:
            # Test with candlesticks category
            response = requests.get(f"{self.api_url}/curriculum/categories/candlesticks/lesson", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('has_lesson'):
                    required_fields = ['title', 'description', 'total_pages', 'pages']
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.log_test("Category Lesson", False, f"Missing fields: {missing_fields}")
                        return False
                    
                    self.log_test("Category Lesson", True)
                    return True
                else:
                    self.log_test("Category Lesson", True, "No lesson available for category")
                    return True
            else:
                self.log_test("Category Lesson", False, f"HTTP {response.status_code}", 200, response.status_code)
                return False
                
        except Exception as e:
            self.log_test("Category Lesson", False, f"Exception: {str(e)}")
            return False

    def test_category_levels(self, user_data=None):
        """Test category levels endpoint"""
        try:
            url = f"{self.api_url}/curriculum/categories/candlesticks/levels"
            if user_data:
                url += f"?user_id={user_data['id']}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    level = data[0]
                    required_fields = ['level', 'is_unlocked', 'is_completed', 'total_exercises', 'completed_exercises']
                    missing_fields = [field for field in required_fields if field not in level]
                    
                    if missing_fields:
                        self.log_test("Category Levels", False, f"Missing fields: {missing_fields}")
                        return False
                    
                    self.log_test("Category Levels", True)
                    return data
                else:
                    self.log_test("Category Levels", False, "No levels returned or invalid format")
                    return False
            else:
                self.log_test("Category Levels", False, f"HTTP {response.status_code}", 200, response.status_code)
                return False
                
        except Exception as e:
            self.log_test("Category Levels", False, f"Exception: {str(e)}")
            return False

    def test_level_exercises(self, user_data=None):
        """Test level exercises endpoint"""
        try:
            url = f"{self.api_url}/curriculum/categories/candlesticks/levels/1/exercises"
            if user_data:
                url += f"?user_id={user_data['id']}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    exercise = data[0]
                    required_fields = ['id', 'question', 'options', 'correct_answer']
                    missing_fields = [field for field in required_fields if field not in exercise]
                    
                    if missing_fields:
                        self.log_test("Level Exercises", False, f"Missing fields: {missing_fields}")
                        return False
                    
                    self.log_test("Level Exercises", True)
                    return True
                else:
                    self.log_test("Level Exercises", False, "No exercises returned or invalid format")
                    return False
            else:
                self.log_test("Level Exercises", False, f"HTTP {response.status_code}", 200, response.status_code)
                return False
                
        except Exception as e:
            self.log_test("Level Exercises", False, f"Exception: {str(e)}")
            return False

    def test_curriculum_tiers(self):
        """Test curriculum tiers endpoint"""
        try:
            response = requests.get(f"{self.api_url}/curriculum/tiers", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    tier = data[0]
                    required_fields = ['id', 'name', 'categories']
                    missing_fields = [field for field in required_fields if field not in tier]
                    
                    if missing_fields:
                        self.log_test("Curriculum Tiers", False, f"Missing fields: {missing_fields}")
                        return False
                    
                    self.log_test("Curriculum Tiers", True)
                    return True
                else:
                    self.log_test("Curriculum Tiers", False, "No tiers returned or invalid format")
                    return False
            else:
                self.log_test("Curriculum Tiers", False, f"HTTP {response.status_code}", 200, response.status_code)
                return False
                
        except Exception as e:
            self.log_test("Curriculum Tiers", False, f"Exception: {str(e)}")
            return False

    def test_seed_demo_user(self):
        """Test creating/checking demo user"""
        try:
            response = requests.post(f"{self.api_url}/seed/test-user", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('email') == 'demo@tradelingo.com':
                    self.log_test("Seed Demo User", True)
                    return True
                else:
                    self.log_test("Seed Demo User", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Seed Demo User", False, f"HTTP {response.status_code}", 200, response.status_code)
                return False
                
        except Exception as e:
            self.log_test("Seed Demo User", False, f"Exception: {str(e)}")
            return False

    def test_real_market_assets(self):
        """Test Real Market assets endpoint"""
        try:
            response = requests.get(f"{self.api_url}/real-market/assets", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    asset = data[0]
                    required_fields = ['id', 'name', 'type']
                    missing_fields = [field for field in required_fields if field not in asset]
                    
                    if missing_fields:
                        self.log_test("Real Market Assets", False, f"Missing fields: {missing_fields}")
                        return False
                    
                    self.log_test("Real Market Assets", True)
                    return data
                else:
                    self.log_test("Real Market Assets", False, "No assets returned or invalid format")
                    return False
            else:
                self.log_test("Real Market Assets", False, f"HTTP {response.status_code}", 200, response.status_code)
                return False
                
        except Exception as e:
            self.log_test("Real Market Assets", False, f"Exception: {str(e)}")
            return False

    def test_real_market_start_session(self, user_id="d5660ecf-239a-4e59-b6e9-f75fe6d5654f"):
        """Test Real Market start session endpoint"""
        try:
            session_data = {
                "user_id": user_id,
                "asset": "EURUSD"
            }
            
            response = requests.post(
                f"{self.api_url}/real-market/start-session",
                json=session_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['session_id', 'asset', 'candles', 'current_index', 'total_candles']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Real Market Start Session", False, f"Missing fields: {missing_fields}")
                    return False
                
                # Check if candles are properly formatted
                if not isinstance(data.get('candles'), list) or len(data['candles']) == 0:
                    self.log_test("Real Market Start Session", False, "No candles returned")
                    return False
                
                candle = data['candles'][0]
                candle_fields = ['timestamp', 'open', 'high', 'low', 'close']
                missing_candle_fields = [field for field in candle_fields if field not in candle]
                
                if missing_candle_fields:
                    self.log_test("Real Market Start Session", False, f"Missing candle fields: {missing_candle_fields}")
                    return False
                
                self.log_test("Real Market Start Session", True)
                return data
            else:
                try:
                    error_data = response.json()
                    self.log_test("Real Market Start Session", False, f"HTTP {response.status_code}: {error_data}", 200, response.status_code)
                except:
                    self.log_test("Real Market Start Session", False, f"HTTP {response.status_code}: {response.text}", 200, response.status_code)
                return False
                
        except Exception as e:
            self.log_test("Real Market Start Session", False, f"Exception: {str(e)}")
            return False

    def test_real_market_advance_candle(self, session_id):
        """Test Real Market advance candle endpoint"""
        try:
            response = requests.post(
                f"{self.api_url}/real-market/advance-candle?session_id={session_id}",
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                # Check if response has expected structure
                if 'finished' in data:
                    if data.get('finished'):
                        self.log_test("Real Market Advance Candle", True, "Session finished")
                    else:
                        required_fields = ['new_candle', 'current_index']
                        missing_fields = [field for field in required_fields if field not in data]
                        
                        if missing_fields:
                            self.log_test("Real Market Advance Candle", False, f"Missing fields: {missing_fields}")
                            return False
                        
                        # Check new candle structure
                        candle = data['new_candle']
                        candle_fields = ['timestamp', 'open', 'high', 'low', 'close']
                        missing_candle_fields = [field for field in candle_fields if field not in candle]
                        
                        if missing_candle_fields:
                            self.log_test("Real Market Advance Candle", False, f"Missing candle fields: {missing_candle_fields}")
                            return False
                    
                    self.log_test("Real Market Advance Candle", True)
                    return data
                else:
                    self.log_test("Real Market Advance Candle", False, "Missing 'finished' field in response")
                    return False
            else:
                try:
                    error_data = response.json()
                    self.log_test("Real Market Advance Candle", False, f"HTTP {response.status_code}: {error_data}", 200, response.status_code)
                except:
                    self.log_test("Real Market Advance Candle", False, f"HTTP {response.status_code}: {response.text}", 200, response.status_code)
                return False
                
        except Exception as e:
            self.log_test("Real Market Advance Candle", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all backend tests"""
        print(f"🚀 Starting TradeLingo Backend API Tests")
        print(f"📍 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Test basic connectivity
        if not self.test_health_endpoint():
            print("❌ Health check failed - stopping tests")
            return self.generate_report()
        
        if not self.test_root_endpoint():
            print("❌ Root endpoint failed - continuing with other tests")
        
        # Test demo user creation/existence
        self.test_seed_demo_user()
        
        # Test authentication
        user_data = self.test_specific_user_login()
        self.test_invalid_login()
        
        # Test curriculum endpoints
        self.test_curriculum_tiers()
        
        # Test category-specific endpoints (new book/lesson functionality)
        self.test_category_lesson(user_data)
        levels_data = self.test_category_levels(user_data)
        self.test_level_exercises(user_data)
        
        # Test lessons (with and without user)
        self.test_lessons_endpoint()
        if user_data:
            self.test_lessons_endpoint(user_data)
        
        # Test Real Market endpoints
        print("\n📈 Testing Real Market Endpoints...")
        assets_data = self.test_real_market_assets()
        
        # Test session creation and candle advancement
        session_data = self.test_real_market_start_session()
        if session_data:
            self.test_real_market_advance_candle(session_data.get('session_id'))
        
        return self.generate_report()

    def generate_report(self):
        """Generate test report"""
        print("\n" + "=" * 60)
        print(f"📊 TEST SUMMARY")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%" if self.tests_run > 0 else "0%")
        
        if self.tests_passed < self.tests_run:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  • {result['test_name']}: {result['details']}")
        
        return {
            "total_tests": self.tests_run,
            "passed_tests": self.tests_passed,
            "failed_tests": self.tests_run - self.tests_passed,
            "success_rate": (self.tests_passed/self.tests_run*100) if self.tests_run > 0 else 0,
            "test_results": self.test_results
        }

def main():
    tester = TradeLingoBE_Tester()
    report = tester.run_all_tests()
    
    # Return appropriate exit code
    if report["failed_tests"] == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {report['failed_tests']} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())