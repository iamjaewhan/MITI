from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status, test

class UserUpdateAPITestCase(test.APITestCase):
    
    def set_url(self, user):
        self.url = reverse('user_update', kwargs={'user_id': user['id']})
    
    def set_token(self, user):
        data = {
            "email": user['email'],
            "password": user['password']
        }
        response = self.client.post(reverse('login'), data, format='json')
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.access_token)
        
    def login_by(self, user):
        self.set_token(user)
        self.set_url(user)
        
    def login_and_delete(self, user):
        response = self.client.post(reverse('login'), user, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ response.data['access'])
        self.client.delete(reverse('user_update', kwargs={'user_id':user['id']}), format='json')
        self.client.credentials(HTTP_AUTHORIZATION='')
    
    @classmethod
    def create_superuser_data(cls):
        data = {
            "email": "admin@admin.com",
            "username": "adminuser",
            "password": "Adminuser123#",
            "password_check": "Adminuser123#"
        }   
        admin_user = get_user_model().objects.create_superuser(**data)
        data['id'] = admin_user.id
        return data
    
    @classmethod
    def create_user_data(cls, number):
        data = {
            "email": f'Testuser{number}@testuser.com',
            "username": f'testuser{number}',
            "password": 'Testuser123#',
            "password_check": 'Testuser123#'
        }
        user = get_user_model().objects.create_user(**data)
        data['id'] = user.id
        return data
    
    @classmethod
    def setUpTestData(cls):
        cls.users = []
        cls.users.append(cls.create_superuser_data())
        for i in range(1,6):
            cls.users.append(cls.create_user_data(i)) 

    #정상 회원정보 수정 케이스
    def test_givenValidUserData_whenRequestingUserinfoUpdate_thenReturns200Response(self):
        # Given
        self.login_by(self.users[1])
        data = {
            "email": "modifiedemail@testuser.com",
            "username": "modifiedusername",
            "password": self.users[1]['password'],
            "new_password": "NewPassowrd123#"
        }
        
        # When
        response = self.client.patch(self.url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['username'], data['username'])
        self.assertIsInstance(response.data['id'], int)
        
    # 유효하지 않은 요청
    # 1. 존재하지 않는 user_id
    def test_givenNonExistingUserId_whenRequestingUserInfoUpdate_thenReturns404Response(self):
        # Given
        self.login_by(self.users[1])
        data = {
            "email": "modifiedemail@testuser.com",
            "username": "modified_username",
            "password": "Testuser123#",
            "new_password": "NewPassowrd123#"
        }
        url = reverse('user_update', kwargs={'user_id': 4294000000})
        
        # When
        response = self.client.patch(url, data, format='json')

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    # 2. 로그인되지 않은 사용자의 요청
    def test_givenUnauthorizedValidData_whenRequestingUserInfoUpdate_thenReturns401Response(self):
        # Given
        data = {
            "email": "modifiedemail@testuser.com",
            "username": "modified_username",
            "password": "Testuser123#",
            "new_password": "NewPassowrd123#"
        }
        self.set_url(self.users[1])

        # When
        response = self.client.patch(self.url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    # 3. 수정 user와 요청 user 불일치
    def test_givenValidData_whenRequestingNotOwningUserInfoUpdate_thenReturns403Resonse(self):
        # Given
        self.login_by(self.users[1])
        data = {
            "email": "modifiedemail@testuser.com",
            "password": "Testuser123#",
        }
        url = reverse('user_update', kwargs={'user_id': self.users[2]['id']})

        # When
        response = self.client.patch(url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # 유효하지 않은 입력값
    # 1. email format
    def test_givenInvalidData_whenRequestingUserInfoUpdate_thenReturns400Response(self):
        # Given
        self.login_by(self.users[1])
        data = {
            "email": "invalidEmailFormanttestuser.com",
            "password": "Testuser123#",
        }
        
        # When
        response = self.client.patch(self.url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 2. existing email
    def test_givenDuplicatedEmailData_whenRequestingUserInfoUpdate_thenReturns400Response(self):
        # Given
        self.login_by(self.users[1])
        data = {
            "email": self.users[2]['email'],
            "password": "Testuser123#",
        }
        
        # When
        response = self.client.patch(self.url, data, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    # 3. existing username
    def test_givenDuplicatedUsernameData_whenRequestingUserInfoUpdate_thenReturns400Response(self):
        # Given
        self.login_by(self.users[1])
        data = {
            "username": self.users[2]['username'],
            "password": "Testuser123#",
        }

        # When
        response = self.client.patch(self.url, data, format='json')
        print(response.data)
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
        
    #회원정보 삭제 정상 케이스
    def test_givenUserId_whenRequestingAccountDeletion_thenReturns200Response(self):
        # Given
        self.login_by(self.users[1])
        
        # When
        response = self.client.delete(self.url, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    #유효하지 않은 요청
    # 1. 존재하지 않는 user_id 
    def test_givenInvalidUserId_whenRequestingAccountDeletion_thenReturns404Response(self):
        # Given
        self.login_by(self.users[1])
        url = reverse('user_update', kwargs={'user_id': 4294000000})
        
        # When
        response = self.client.delete(url, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    # 2. 삭제 user와 요청 user 불일치
    def test_givenValidUserId_whenRequestingNotOwningAccountDeletion_thenReturns403Response(self):
        # Given
        self.login_by(self.users[1])
        url = reverse('user_update', kwargs={'user_id': self.users[2]['id']})

        # When
        response = self.client.delete(url, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    #회원정보 복구 정상 케이스
    def test_givenUserId_whenRequestingAccountRestoration_thenReturns200Response(self):
        # # Given
        self.login_and_delete(self.users[1])
        self.login_by(self.users[0])
        url = reverse('user_update', kwargs={'user_id': self.users[1]['id']})
        
        # When
        response = self.client.put(url, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # 유효하지 않은 요청
    # 1. 삭제되지 않거나 존재하지 않는 user_id
    def test_givenInvalidUserId_whenRequestingAccountRestoration_thenReturns404Response(self):
        # Given
        self.login_by(self.users[0])
        url = reverse('user_update', kwargs={'user_id': self.users[1]['id']})
        
        # When
        response = self.client.put(url, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    # 2. 권한없음
    def test_givenValidUserId_whenRequestingNotOwningAccountRestoration_thenReturns403Response(self):
        # Given
        self.login_by(self.users[1])
        url = reverse('user_update', kwargs={'user_id': self.users[2]['id']})
        
        # When
        response = self.client.patch(url, format='json')
        
        # Then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        
        