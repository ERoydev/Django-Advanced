import os
import django

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'templatesLecture.settings')  # Adjust to your project
django.setup()

# Import Django components only after setup
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse
from templatesLecture.views import IndexView

UserModel = get_user_model()


class TestIndexViewIntegration(TestCase):

    def setUp(self):
        self.credentials = {
            "username": "emilchoroydev",
            "email": "randomemail@gmail.com",
            "password": "Test123!",
        }

    def test_authenticated_user_returns_auth_template(self):
        # Create an authenticated user
        user = UserModel.objects.create_user(
            **self.credentials
        )

        self.client.login(**self.credentials)

        # Call the view
        response = self.client.get(reverse('home'))

        # Assert the correct template is used
        self.assertEqual(response.template_name, ['common/logged_in.html'])

    def test_unauthenticated_user_returns_home_template(self):
        # Call the view
        response = self.client.get(reverse('home'))

        # Assert the correct template is used
        self.assertEqual(response.template_name, ['home.html'])


class TestIndexViewUnit(TestCase):
    """
    This TestCase creates a temporary database for testing.

    CLOSER TO UNIT TEST testing -> faster doesn't test middlewares

    Mocks the request with RequestFactory()
    """

    def setUp(self):
        # Use RequestFactory for mock requests
        self.factory = RequestFactory()
        self.credentials = {
            "username": "emilchoroydev",
            "email": "e.roydev@gmail.com",
            "password": "Test123!",
        }

    def test_authenticated_user_returns_auth_template(self):
        # Create an authenticated user
        user = UserModel.objects.create_user(**self.credentials)
        request = self.factory.get(reverse('home'))
        request.user = user

        # Call the view
        response = IndexView.as_view()(request)

        # Assert the correct template is used
        self.assertEqual(response.template_name, ['common/logged_in.html'])

    def test_unauthenticated_user_returns_home_template(self):
        request = self.factory.get(reverse('home'))
        request.user = AnonymousUser()

        # Call the view
        response = IndexView.as_view()(request)

        # Assert the correct template is used
        self.assertEqual(response.template_name, ['home.html'])
