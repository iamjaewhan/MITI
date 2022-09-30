from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status, test

class UserLoginAPITestCase(test.APITestCase):
    url = reverse('login')
    
    @classmethod
    def setUpTestData(cls):
        data = {
            "email": "testuser@testuser.com",
            "username": "testuser",
            "password": "Testuser123#",
            "password_check": "Testuser123#"
        }
        get_user_model().objects.create_user(**data)

    #정상 로그인 케이스
    def test_givenValidData_whenRequestingLogin_thenReturns200Response(self):
        # Given
        data = {
            "email": "testuser@testuser.com",
            "password": "Testuser123#"
        }
        
        # When
        response = self.client.post(self.url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
        self.assertIsInstance(response.data['id'], int)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        
    # 유효하지 않은 입력값
    # 1. email format
    def test_givenInvalidEmail_whenRequestingLogin_thenReturns400Response(self):
        # Given
        data = {
            "email": "testusertestusercom",
            "password": "Testuser123#"
        }
        
        # When
        response = self.client.post(self.url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    # 2. password format
    def test_givenInvalidPassword_whenRequestingLogin_thenReturns400Response(self):
        # Given
        data = {
            "email": "testuser@testuser.com",
            "password": "testpassword"
        }
        
        # When
        response = self.client.post(self.url, data, format='json')

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # 로그인 정보 불일치
    # 1. 존재하지 않는 email
    def test_givenNonexistingEmail_whenRequestingLogin_thenReturns400Response(self):
        # Given
        data = {
            "email": "nonexistingemail@testuser.com",
            "password": "testpassword"
        }
        
        # When
        response = self.client.post(self.url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    # 2. 잘못된 password
    def test_given_when_then(self):
        # Given
        data = {
            "email": "testuser@testuser.com",
            "password": "testpassword"
        }
        
        # When
        response = self.client.post(self.url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)