from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status, test

class UserSignupAPITestCase(test.APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        data = {
            "email": "duplicateduser@testuser.com",
            "username": "duplicateduser",
            "password": "Testuser123#",
            "password_check": "Testuser123#"
        }
        get_user_model().objects.create_user(**data)
        cls.url = reverse('signup')

    
    #정상 회원가입 케이스
    def test_givenValidData_whenRequestSignup_returns201Response(self):
        # Given
        data = {
            "email": "testuser@user.com",
            "username": "testuser",
            "password": "Testuser1234#",
            "password_check": "Testuser1234#"
        }
        
        # When
        response = self.client.post(self.url, data, format='json')
        # Then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data['id'], int)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['username'], data['username'])
        
        
    
    # 유효하지 않은 입력 케이스
    # 1. email format
    def test_givenInvalidEmail_whenRequestSignup_thenReturns400Response(self):
        # Given
        data = {
            "email": "testuser",
            "username": "testuser",
            "password": "Testuser1234#",
            "password_check": "Testuser1234#"
        }
        
        # When
        response = self.client.post(self.url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    # 2. password, password_check format
    def test_givenInvalidPassword_whenRequestingSignup_thenReturns400Response(self):
        # Given
        data = {
            "email": "testuser@testuser.com",
            "username": "testuser",
            "password": "invalidpw",
            "password_check": "invalidpw"
        }
        
        # When
        response = self.client.post(self.url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # 3. password, password_check match or not
    def test_givenUnidenticalPassWordk_whenRequestingSignup_thenReturns400Response(self):
        # Given
        data = {
            "email": "testuser@testuser.com",
            "username": "testuser",
            "password": "Testuser123#",
            "password_check": "notmatch123#"
        }
        
        # When
        response = self.client.post(self.url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # DB integrity
    # 1. existing email
    def test_givenDuplicatedEmail_whenRequestingSignup_thenReturns400Response(self):
        # Given
        data = {
            "email": "duplicateduser@testuser.com",
            "username": "testuser",
            "password": "Testuser123#",
            "password_check": "Testuser123#"
        }
        
        # When
        response = self.client.post(self.url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                
        
    # 2. existing username
    def test_givenDuplicatedUsername_whenRequestingSignup_thenReturns400Response(self):
        # Given
        data = {
            "email": "testuser@testuser.com",
            "username": "duplicateduser",
            "password": "Testuser123#",
            "password_check": "Testuser123#"
        }
        
        # When
        response = self.client.post(self.url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        