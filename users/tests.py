from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.

User = get_user_model()

class RegisterViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register') 
        self.valid_payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPassword123",
            "confirm_password": "StrongPassword123",
            "user_type": "client"
        }
        self.invalid_payload = {
            "username": "newuser",
            "email": "invalidemail", 
            "password": "password",
            "confirm_password": "password",
            "user_type": "client"
        }

    def test_register_user_success(self):
        # Test user registration with valid details
        response = self.client.post(self.register_url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], "User registered successfully.")

    def test_register_user_password_mismatch(self):
        # Test registration when passwords do not match
        payload = self.valid_payload.copy()
        payload['confirm_password'] = 'DifferentPassword123'
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Check in 'non_field_errors'
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], 'Passwords do not match.')

    def test_register_user_invalid_email(self):
        # Test user registration with invalid email format
        response = self.client.post(self.register_url, self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class LoginViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login') 
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='StrongPassword123', user_type='client')

    def test_login_success(self):
        # Test user login with valid credentials
        response = self.client.post(self.login_url, {"email": "testuser@example.com", "password": "StrongPassword123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_login_invalid_password(self):
        # Test user login with incorrect password
        response = self.client.post(self.login_url, {"email": "testuser@example.com", "password": "WrongPassword"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid email or password')

    def test_login_invalid_email(self):
        # Test user login with wrong email
        response = self.client.post(self.login_url, {"email": "wrongemail@example.com", "password": "StrongPassword123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid email or password')


class LogoutViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='StrongPassword123', user_type='client')
        self.refresh = RefreshToken.for_user(self.user)
        self.logout_url = reverse('logout') 

    def test_logout_success(self):
        # Test successful logout with valid refresh token
        response = self.client.post(self.logout_url, {"refresh_token": str(self.refresh)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], 'logged out')

    def test_logout_invalid_token(self):
        # Test logout with invalid refresh token
        response = self.client.post(self.logout_url, {"refresh_token": "invalidtoken"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_logout_no_token(self):
        # Test logout without providing refresh token
        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Refresh token is required.')
