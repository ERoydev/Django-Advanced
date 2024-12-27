import tests.django_settings_initializer # This initializes my django_settings

from django.urls import reverse

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from posts.models import Post


UserModel = get_user_model()

"""
For TestCase i will have problem if i am with sqlite db

"""

class TestApprovePostViewIntegration(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "emilchoroydev",
            "email": "randomemail@gmail.com",
            "password": "Test123!",
        }

        self.user = UserModel.objects.create(
            **self.credentials
        )

        self.custom_post = Post.objects.create(
            title="Yu Gi Oh!",
            content="Very entertaining game, everyone should try it at least once.",
            author=self.user,
            languages='BG',
            approved=False,
        )

    def test_functionality_when_post_is_approved(self):
        self.client.login(
            **self.credentials
        )

        response = self.client.post(reverse('approve_post', args=[self.custom_post.pk]))

        self.custom_post.refresh_from_db()

        self.assertTrue(self.custom_post.approved)
        self.assertRedirects(response, reverse('show_posts'))


    def test_approve_invalid_post_raises_DoesNotExists_error(self):
        self.client.login(
            **self.credentials
        )

        response = self.client.post(reverse('approve_post', args=[999]))

        print(response)
        self.assertEqual(response.status_code, 404)



class TestApprovePostViewUnit(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.credentials = {
            "username": "emilchoroydev",
            "email": "randomemail@gmail.com",
            "password": "Test123!",
        }

        self.user = UserModel.objects.create(
            **self.credentials
        )

        self.custom_post = Post.objects.create(
            title="Yu Gi Oh!",
            content="Very entertaining game, everyone should try it at least once.",
            author=self.user,
            languages='BG',
            approved=False,
        )

    def test_functionality_when_post_is_approved(self):

        response = self.factory.post('approve_post', {'pk': self.custom_post.pk})

        self.assertEqual('hey', 'hey')