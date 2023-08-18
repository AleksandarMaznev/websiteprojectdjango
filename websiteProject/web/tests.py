import unittest
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from websiteProject.web.forms import CommentForm, UserCreationForm, LoginForm
from websiteProject.web.models import Profile, Book, Comment, Rating


# Create your tests here.


class CommentFormTest(TestCase):

    def test_valid_form(self):
        data = {
            'content': 'Test comment content',
        }
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())


class CommentViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)
        self.book = Book.objects.create(title='Test Book', author=self.profile)


    def test_comment_post(self):
        client = Client()
        client.login(username='testuser', password='testpassword')

        data = {
            'content': 'Test comment content',
        }

        response = client.post(reverse('book_comment', args=[self.book.pk]), data=data)
        self.assertEqual(response.status_code, 302)

        comment = Comment.objects.last()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.content, data['content'])
        self.assertEqual(comment.book_commented_on, self.book)
        self.assertEqual(comment.posted_by, self.profile)
        self.assertIsNotNone(comment.posted_on)

    def test_comment_get(self):
        client = Client()
        client.login(username='testuser', password='testpassword')

        response = client.get(reverse('book_comment', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This story has no comments yet!')


class UserCreationFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = UserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'mismatchedpassword',
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('password2', form.errors)

    def test_save_method(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(User.objects.filter(username='testuser').exists())


class LoginFormTest(TestCase):

    def test_blank_login_form(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)


class RatingModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', id=1)
        profile = Profile.objects.create(username='testuser', user_id=1, id=1)
        book = Book.objects.create(title='Test Book', id=1, author_id= 1)
        Rating.objects.create(profile=profile, book=book, rate=4)

    def test_rating_creation(self):
        rating = Rating.objects.get(id=1)
        self.assertEqual(rating.profile.username, 'testuser')
        self.assertEqual(rating.book.title, 'Test Book')
        self.assertEqual(rating.rate, 4)

    def test_default_rate_value(self):
        rating = Rating.objects.get(id=1)
        self.assertEqual(rating.rate, 4)

    def test_str_representation(self):
        rating = Rating.objects.get(id=1)
        self.assertEqual(str(rating), f"{rating.profile.username} - {rating.book.title}: {rating.rate}")


if __name__ == '__main__':
    unittest.main()
