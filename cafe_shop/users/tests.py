from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from .forms import RegisterForm

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_profile_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.__str__(), 'Профиль testuser')

class RegisterFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='testpass123'
        )
        form_data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_post(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)