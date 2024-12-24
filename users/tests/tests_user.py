from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test1@example.com',
            'password': 'vakhed.1',
            'name': 'test',
            'surname': 'user'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        """create user"""
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        """superuser create"""
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='AdminStrongPassword123!'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_without_email(self):
        """email siz user"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='test123')

    def test_user_string_representation(self):
        """check the user for string"""
        self.assertEqual(str(self.user), f"{self.user.name} {self.user.surname}")

    def test_email_uniqueness(self):
        """non-repetition for email"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test1@example.com',
                password='AnotherStrongPassword123!',
                name='Another',
                surname='User'
            )


class CustomUserAPITestCase(TestCase):
    def setUp(self):
        """API testlari uchun sozlama"""
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'email': 'test@example.com',
            'password': 'vakhed.1',
            'password2': 'vakhed.1',
            'name': 'Test',
            'surname': 'User'
        }

    def test_user_registration_success(self):
        """user royhatdan otgani tekshirish"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())

    def test_user_registration_duplicate_email(self):
        """test duplicate email """
        # Birinchi marta login
        self.client.post(self.register_url, self.user_data)

        # 2nchi marta xuddi shu email bilan login qiliw
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_password_mismatch(self):
        """password lar mos kelishi """
        mismatched_data = self.user_data.copy()
        mismatched_data['password2'] = 'DifferentPassword123!'

        response = self.client.post(self.register_url, mismatched_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_invalid_email(self):
        """wrong email bn login qiliw"""
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'invalid-email'

        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        """success login check"""
        # user ni royxatdan o'tkaziw
        self.client.post(self.register_url, self.user_data)
        # login
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_failure(self):
        """failed login check"""
        # royxatdan otmagan user bn login
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_incorrect_password(self):
        """wrong password bn login"""
        self.client.post(self.register_url, self.user_data)
        login_data = {
            'email': self.user_data['email'],
            'password': 'IncorrectPassword123!'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
