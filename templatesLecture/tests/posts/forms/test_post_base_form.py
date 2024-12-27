import tests.django_settings_initializer # This initializes my django_settings

from django.test import TestCase
from django.contrib.auth import get_user_model

from posts.forms import PostBaseForm


class TestPostBaseFormUnit(TestCase):

    def setUp(self):
        self.valid_data = {
            "title":"valid data",
            "content":"This is the content",
            "languages":'BG',
        }


    def test__form_is_valid_expect_true(self):
        form = PostBaseForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test__empty_title__returns_error(self):
        self.valid_data['title'] = ''
        form = PostBaseForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test__title_too_long__returns_error(self):
        self.valid_data['title'] = 'asdadadadawdawdwdawdawdawfsdfsdfsdfsdscfsefsefsefsefsefsesesefsefsefsefsefsefsefsesefsefsefsefsefsefsefse'
        form = PostBaseForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test__title_content_contains_title__returns_validationError(self):
        self.valid_data['title'] = 'a'
        self.valid_data['content'] = 'acdb'
        form = PostBaseForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIsNotNone(form.errors)

    def test__save_method_capitalizes_title__expect_valid(self):
        self.valid_data['title'] = 'hello'
        form = PostBaseForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

        post = form.save(commit=False)

        self.assertEqual(
            post.title,
            self.valid_data['title'].capitalize(),
        )