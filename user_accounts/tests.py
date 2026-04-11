from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class AuthTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_register(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@test.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login(self):
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_logout(self):
        User.objects.create_user(
            username='logoutuser',
            password='testpass123'
        )
        login_response = self.client.post('/api/auth/login/', {
            'username': 'logoutuser',
            'password': 'testpass123'
        })
        access = login_response.data['access']
        refresh = login_response.data['refresh']
        
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access}'
        )
        response = self.client.post('/api/auth/logout/', {
            'refresh': refresh
        })
        print(response.data)
        self.assertEqual(response.status_code, 200)