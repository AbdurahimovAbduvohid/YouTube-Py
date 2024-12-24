from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError


User = get_user_model()


class JWTTokenTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user_data = {
            'email': 'tokentest@example.com',
            'password': 'vakhed.1',
            'name': 'Token',
            'surname': 'Tester'
        }
        # create user
        self.user = User.objects.create_user(**self.user_data)

    def test_obtain_jwt_token(self):
        """get token"""
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })

        # check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('email', response.data)

    def test_token_validation(self):
        # Get a token via login
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })

        # get access va refresh token
        access_token = response.data['access']
        refresh_token = response.data['refresh']

        try:
            # access token confirm
            validated_access_token = AccessToken(access_token)
            self.assertTrue(validated_access_token['user_id'], self.user.id)

            # refresh token confirm
            RefreshToken(refresh_token)
        except TokenError:
            self.fail("Token validation failed")

    def test_invalid_token_login(self):
        """check for login with failed token"""
        invalid_token = "invalid.jwt.token"
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {invalid_token}')

        # get user information
        response = self.client.get(reverse('user-list'))

        # check 401 unauthorized status
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        """refresh token"""
        # login orqali refresh token olish
        login_response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })

        # Refresh token URL (JWT kutubxonasidan kelib chiqadi)
        refresh_url = reverse('token_refresh')

        # Token update
        refresh_response = self.client.post(refresh_url, {
            'refresh': login_response.data['refresh']
        })

        # get new access token
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

