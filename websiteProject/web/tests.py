import unittest

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from websiteProject.web.forms import CommentForm
from websiteProject.web.models import Profile, Book, Comment


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













if __name__ == '__main__':
    unittest.main()
