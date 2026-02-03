#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for B2B Mobile Application
Tests all authentication and dashboard endpoints with various scenarios
"""

import requests
import json
import time
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "https://b2border-4.preview.emergentagent.com/api"
HEADERS = {"Content-Type": "application/json"}

class BackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS.copy()
        self.test_results = []
        self.test_users = {}
        self.tokens = {}
        
    def log_test(self, test_name: str, success: bool, details: str, response_data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "response_data": response_data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        if response_data and not success:
            print(f"   Response: {response_data}")
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, token: str = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy()
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            else:
                return False, {"error": f"Unsupported method: {method}"}, 0
            
            try:
                response_data = response.json()
            except:
                response_data = {"text": response.text}
            
            return response.status_code < 400, response_data, response.status_code
            
        except requests.exceptions.RequestException as e:
            return False, {"error": str(e)}, 0
    
    def test_user_registration(self):
        """Test user registration with various scenarios"""
        print("\n=== Testing User Registration ===")
        
        # Test data for different roles
        test_users_data = [
            {
                "name": "admin_user",
                "data": {
                    "email": "admin@techcorp.com",
                    "mobile": "+1234567890",
                    "password": "SecurePass123!",
                    "name": "John Admin",
                    "role": "Admin",
                    "company_name": "TechCorp Solutions"
                }
            },
            {
                "name": "sales_user",
                "data": {
                    "email": "sales@techcorp.com",
                    "mobile": "+1234567891",
                    "password": "SalesPass456!",
                    "name": "Jane Sales",
                    "role": "Sales",
                    "company_name": "TechCorp Solutions"
                }
            },
            {
                "name": "buyer_user",
                "data": {
                    "email": "buyer@retailco.com",
                    "mobile": "+1234567892",
                    "password": "BuyerPass789!",
                    "name": "Mike Buyer",
                    "role": "Buyer",
                    "company_name": "RetailCo Inc"
                }
            }
        ]
        
        # Test successful registrations
        for user_info in test_users_data:
            success, response, status_code = self.make_request("POST", "/auth/register", user_info["data"])
            
            if success and "access_token" in response:
                self.test_users[user_info["name"]] = user_info["data"]
                self.tokens[user_info["name"]] = response["access_token"]
                self.log_test(
                    f"Register {user_info['data']['role']} user",
                    True,
                    f"Successfully registered {user_info['data']['name']} with role {user_info['data']['role']}"
                )
                
                # Verify password is not returned in response
                if "password" in str(response):
                    self.log_test(
                        f"Password security check for {user_info['data']['role']}",
                        False,
                        "Password found in registration response - security issue"
                    )
                else:
                    self.log_test(
                        f"Password security check for {user_info['data']['role']}",
                        True,
                        "Password not exposed in response"
                    )
            else:
                self.log_test(
                    f"Register {user_info['data']['role']} user",
                    False,
                    f"Failed to register {user_info['data']['name']}: {response}",
                    response
                )
        
        # Test registration without company name
        no_company_data = {
            "email": "nocompany@example.com",
            "mobile": "+1234567893",
            "password": "NoCompPass123!",
            "name": "No Company User",
            "role": "Buyer"
        }
        success, response, status_code = self.make_request("POST", "/auth/register", no_company_data)
        self.log_test(
            "Register without company name",
            success,
            "Registration without company name should work with default company" if success else f"Failed: {response}"
        )
        
        # Test duplicate email validation
        duplicate_email_data = {
            "email": "admin@techcorp.com",  # Same as admin user
            "mobile": "+1234567894",
            "password": "DupePass123!",
            "name": "Duplicate Email User",
            "role": "Sales",
            "company_name": "Another Company"
        }
        success, response, status_code = self.make_request("POST", "/auth/register", duplicate_email_data)
        self.log_test(
            "Duplicate email validation",
            not success and status_code == 400,
            "Should reject duplicate email" if not success else "Failed to reject duplicate email",
            response
        )
        
        # Test duplicate mobile validation
        duplicate_mobile_data = {
            "email": "unique@example.com",
            "mobile": "+1234567890",  # Same as admin user
            "password": "DupeMobile123!",
            "name": "Duplicate Mobile User",
            "role": "Sales",
            "company_name": "Another Company"
        }
        success, response, status_code = self.make_request("POST", "/auth/register", duplicate_mobile_data)
        self.log_test(
            "Duplicate mobile validation",
            not success and status_code == 400,
            "Should reject duplicate mobile" if not success else "Failed to reject duplicate mobile",
            response
        )
        
        # Test invalid email format
        invalid_email_data = {
            "email": "invalid-email-format",
            "mobile": "+1234567895",
            "password": "InvalidEmail123!",
            "name": "Invalid Email User",
            "role": "Buyer",
            "company_name": "Test Company"
        }
        success, response, status_code = self.make_request("POST", "/auth/register", invalid_email_data)
        self.log_test(
            "Invalid email format validation",
            not success and status_code == 422,
            "Should reject invalid email format" if not success else "Failed to reject invalid email",
            response
        )
        
        # Test invalid mobile format
        invalid_mobile_data = {
            "email": "validmobile@example.com",
            "mobile": "123",  # Too short
            "password": "InvalidMobile123!",
            "name": "Invalid Mobile User",
            "role": "Buyer",
            "company_name": "Test Company"
        }
        success, response, status_code = self.make_request("POST", "/auth/register", invalid_mobile_data)
        self.log_test(
            "Invalid mobile format validation",
            not success and status_code == 400,
            "Should reject invalid mobile format" if not success else "Failed to reject invalid mobile",
            response
        )
        
        # Test missing required fields
        missing_fields_data = {
            "email": "missing@example.com",
            "password": "MissingFields123!",
            "role": "Buyer"
            # Missing mobile and name
        }
        success, response, status_code = self.make_request("POST", "/auth/register", missing_fields_data)
        self.log_test(
            "Missing required fields validation",
            not success and status_code == 422,
            "Should reject missing required fields" if not success else "Failed to reject missing fields",
            response
        )
        
        # Test invalid role
        invalid_role_data = {
            "email": "invalidrole@example.com",
            "mobile": "+1234567896",
            "password": "InvalidRole123!",
            "name": "Invalid Role User",
            "role": "InvalidRole",
            "company_name": "Test Company"
        }
        success, response, status_code = self.make_request("POST", "/auth/register", invalid_role_data)
        self.log_test(
            "Invalid role validation",
            not success and status_code == 400,
            "Should reject invalid role" if not success else "Failed to reject invalid role",
            response
        )
    
    def test_user_login(self):
        """Test user login with various scenarios"""
        print("\n=== Testing User Login ===")
        
        # Test login with email for each role
        for user_name, user_data in self.test_users.items():
            login_data = {
                "login": user_data["email"],
                "password": user_data["password"]
            }
            success, response, status_code = self.make_request("POST", "/auth/login", login_data)
            
            if success and "access_token" in response:
                self.tokens[f"{user_name}_email_login"] = response["access_token"]
                self.log_test(
                    f"Login with email - {user_data['role']}",
                    True,
                    f"Successfully logged in {user_data['name']} with email"
                )
            else:
                self.log_test(
                    f"Login with email - {user_data['role']}",
                    False,
                    f"Failed to login {user_data['name']} with email: {response}",
                    response
                )
        
        # Test login with mobile for each role
        for user_name, user_data in self.test_users.items():
            login_data = {
                "login": user_data["mobile"],
                "password": user_data["password"]
            }
            success, response, status_code = self.make_request("POST", "/auth/login", login_data)
            
            if success and "access_token" in response:
                self.tokens[f"{user_name}_mobile_login"] = response["access_token"]
                self.log_test(
                    f"Login with mobile - {user_data['role']}",
                    True,
                    f"Successfully logged in {user_data['name']} with mobile"
                )
            else:
                self.log_test(
                    f"Login with mobile - {user_data['role']}",
                    False,
                    f"Failed to login {user_data['name']} with mobile: {response}",
                    response
                )
        
        # Test login with incorrect password
        if self.test_users:
            first_user = list(self.test_users.values())[0]
            wrong_password_data = {
                "login": first_user["email"],
                "password": "WrongPassword123!"
            }
            success, response, status_code = self.make_request("POST", "/auth/login", wrong_password_data)
            self.log_test(
                "Login with incorrect password",
                not success and status_code == 401,
                "Should reject incorrect password" if not success else "Failed to reject wrong password",
                response
            )
        
        # Test login with non-existent user
        nonexistent_data = {
            "login": "nonexistent@example.com",
            "password": "SomePassword123!"
        }
        success, response, status_code = self.make_request("POST", "/auth/login", nonexistent_data)
        self.log_test(
            "Login with non-existent user",
            not success and status_code == 401,
            "Should reject non-existent user" if not success else "Failed to reject non-existent user",
            response
        )
        
        # Test login with missing fields
        missing_fields_data = {
            "login": "test@example.com"
            # Missing password
        }
        success, response, status_code = self.make_request("POST", "/auth/login", missing_fields_data)
        self.log_test(
            "Login with missing fields",
            not success and status_code == 422,
            "Should reject missing fields" if not success else "Failed to reject missing fields",
            response
        )
    
    def test_get_current_user(self):
        """Test get current user endpoint"""
        print("\n=== Testing Get Current User ===")
        
        # Test with valid tokens for each user
        for user_name, token in self.tokens.items():
            if not user_name.endswith("_login"):  # Use original tokens, not login tokens
                success, response, status_code = self.make_request("GET", "/auth/me", token=token)
                
                if success and "id" in response:
                    self.log_test(
                        f"Get current user - {user_name}",
                        True,
                        f"Successfully retrieved user data for {user_name}"
                    )
                    
                    # Verify password is not in response
                    if "password" in str(response):
                        self.log_test(
                            f"Password security in /me - {user_name}",
                            False,
                            "Password found in /me response - security issue"
                        )
                    else:
                        self.log_test(
                            f"Password security in /me - {user_name}",
                            True,
                            "Password not exposed in /me response"
                        )
                else:
                    self.log_test(
                        f"Get current user - {user_name}",
                        False,
                        f"Failed to get user data for {user_name}: {response}",
                        response
                    )
        
        # Test with invalid token
        success, response, status_code = self.make_request("GET", "/auth/me", token="invalid_token_12345")
        self.log_test(
            "Get current user with invalid token",
            not success and status_code == 401,
            "Should reject invalid token" if not success else "Failed to reject invalid token",
            response
        )
        
        # Test without token
        success, response, status_code = self.make_request("GET", "/auth/me")
        self.log_test(
            "Get current user without token",
            not success and status_code == 403,
            "Should reject request without token" if not success else "Failed to reject request without token",
            response
        )
        
        # Test with malformed token
        success, response, status_code = self.make_request("GET", "/auth/me", token="malformed.jwt.token")
        self.log_test(
            "Get current user with malformed token",
            not success and status_code == 401,
            "Should reject malformed token" if not success else "Failed to reject malformed token",
            response
        )
    
    def test_dashboard_stats(self):
        """Test dashboard stats endpoint"""
        print("\n=== Testing Dashboard Stats ===")
        
        # Test with each role
        role_tokens = {}
        for user_name, token in self.tokens.items():
            if not user_name.endswith("_login"):
                user_data = self.test_users.get(user_name)
                if user_data:
                    role_tokens[user_data["role"]] = token
        
        for role, token in role_tokens.items():
            success, response, status_code = self.make_request("GET", "/dashboard/stats", token=token)
            
            if success and isinstance(response, dict):
                # Check if response has expected stats structure
                expected_fields = [
                    "total_orders", "pending_orders", "completed_orders",
                    "total_products", "low_stock_products", "total_vendors",
                    "pending_payments", "total_revenue"
                ]
                
                has_all_fields = all(field in response for field in expected_fields)
                
                self.log_test(
                    f"Dashboard stats - {role}",
                    has_all_fields,
                    f"Successfully retrieved dashboard stats for {role}" if has_all_fields else f"Missing fields in stats response for {role}",
                    response if not has_all_fields else None
                )
                
                # Verify placeholder values (should be 0 for Phase 1)
                if has_all_fields:
                    all_zero = all(response[field] == 0 for field in expected_fields)
                    self.log_test(
                        f"Dashboard stats placeholder values - {role}",
                        all_zero,
                        "All stats are placeholder values (0) as expected for Phase 1" if all_zero else "Some stats have non-zero values"
                    )
            else:
                self.log_test(
                    f"Dashboard stats - {role}",
                    False,
                    f"Failed to get dashboard stats for {role}: {response}",
                    response
                )
        
        # Test without authentication
        success, response, status_code = self.make_request("GET", "/dashboard/stats")
        self.log_test(
            "Dashboard stats without authentication",
            not success and status_code == 403,
            "Should reject unauthenticated request" if not success else "Failed to reject unauthenticated request",
            response
        )
    
    def test_users_list(self):
        """Test users list endpoint (Admin only)"""
        print("\n=== Testing Users List (Admin Only) ===")
        
        # Get tokens by role
        admin_token = None
        sales_token = None
        buyer_token = None
        
        for user_name, token in self.tokens.items():
            if not user_name.endswith("_login"):
                user_data = self.test_users.get(user_name)
                if user_data:
                    if user_data["role"] == "Admin":
                        admin_token = token
                    elif user_data["role"] == "Sales":
                        sales_token = token
                    elif user_data["role"] == "Buyer":
                        buyer_token = token
        
        # Test with Admin role (should succeed)
        if admin_token:
            success, response, status_code = self.make_request("GET", "/users", token=admin_token)
            
            if success and isinstance(response, list):
                self.log_test(
                    "Get users list - Admin",
                    True,
                    f"Admin successfully retrieved users list ({len(response)} users)"
                )
                
                # Verify users are from same company
                if response:
                    company_ids = set(user.get("company_id") for user in response if user.get("company_id"))
                    single_company = len(company_ids) <= 1
                    self.log_test(
                        "Users list company isolation - Admin",
                        single_company,
                        "Users list properly filtered by company" if single_company else "Users from multiple companies returned"
                    )
            else:
                self.log_test(
                    "Get users list - Admin",
                    False,
                    f"Admin failed to get users list: {response}",
                    response
                )
        
        # Test with Sales role (should fail with 403)
        if sales_token:
            success, response, status_code = self.make_request("GET", "/users", token=sales_token)
            self.log_test(
                "Get users list - Sales (should fail)",
                not success and status_code == 403,
                "Sales role correctly denied access" if not success else "Sales role incorrectly allowed access",
                response
            )
        
        # Test with Buyer role (should fail with 403)
        if buyer_token:
            success, response, status_code = self.make_request("GET", "/users", token=buyer_token)
            self.log_test(
                "Get users list - Buyer (should fail)",
                not success and status_code == 403,
                "Buyer role correctly denied access" if not success else "Buyer role incorrectly allowed access",
                response
            )
        
        # Test without authentication (should fail with 401)
        success, response, status_code = self.make_request("GET", "/users")
        self.log_test(
            "Get users list without authentication",
            not success and status_code == 403,
            "Unauthenticated request correctly denied" if not success else "Unauthenticated request incorrectly allowed",
            response
        )
    
    def test_jwt_validation(self):
        """Test JWT token validation across endpoints"""
        print("\n=== Testing JWT Token Validation ===")
        
        protected_endpoints = [
            "/auth/me",
            "/dashboard/stats",
            "/users"
        ]
        
        # Test with expired/invalid tokens
        invalid_tokens = [
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ",  # Invalid signature
            "invalid.jwt.format",
            "",
            "Bearer token_without_bearer_prefix"
        ]
        
        for endpoint in protected_endpoints:
            for i, invalid_token in enumerate(invalid_tokens):
                success, response, status_code = self.make_request("GET", endpoint, token=invalid_token)
                self.log_test(
                    f"JWT validation {endpoint} - invalid token {i+1}",
                    not success and status_code in [401, 403],
                    f"Correctly rejected invalid token for {endpoint}" if not success else f"Failed to reject invalid token for {endpoint}",
                    response if success else None
                )
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting B2B Mobile Application Backend Tests")
        print(f"Testing against: {self.base_url}")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run test suites in order
        self.test_user_registration()
        self.test_user_login()
        self.test_get_current_user()
        self.test_dashboard_stats()
        self.test_users_list()
        self.test_jwt_validation()
        
        end_time = time.time()
        
        # Generate summary
        self.generate_summary(end_time - start_time)
    
    def generate_summary(self, duration: float):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"Duration: {duration:.2f} seconds")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS ({failed_tests}):")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['details']}")
        
        print(f"\n✅ PASSED TESTS ({passed_tests}):")
        for result in self.test_results:
            if result["success"]:
                print(f"  • {result['test']}")
        
        # Critical issues summary
        critical_issues = []
        for result in self.test_results:
            if not result["success"] and any(keyword in result["test"].lower() for keyword in ["register", "login", "auth", "token"]):
                critical_issues.append(result)
        
        if critical_issues:
            print(f"\n🚨 CRITICAL ISSUES ({len(critical_issues)}):")
            for issue in critical_issues:
                print(f"  • {issue['test']}: {issue['details']}")
        
        return {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": (passed_tests/total_tests)*100,
            "duration": duration,
            "critical_issues": len(critical_issues)
        }

if __name__ == "__main__":
    tester = BackendTester()
    tester.run_all_tests()