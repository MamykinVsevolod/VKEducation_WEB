from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from app.models import Question, Tag, Profile
from app.views import index, hot, tag, question, ask
from django.utils import timezone


class IndexViewTest(TestCase):
    def test_index_view(self):
        client = Client()
        response = client.get(reverse('index', kwargs={'page': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class HotViewTest(TestCase):
    def test_hot_view(self):
        client = Client()
        response = client.get(reverse('hot', kwargs={'page': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hot.html')

class TagViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.tag = Tag.objects.create(tag='work')

    def test_tag_view(self):
        client = Client()
        response = client.get(reverse('tag', kwargs={'tag_name': self.tag.tag, 'page': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tag.html')


class QuestionViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com',
                                                         password='secret')
        self.profile = Profile.objects.create(user=self.user)
        self.question = Question.objects.create(title='Test Question', text='This is a test question',
                                                date=timezone.now(), profile=self.profile)

    def test_question_view(self):
        client = Client()
        response = client.get(reverse('question', kwargs={'question_id': self.question.id, 'page': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'question.html')


class AskViewTest(TestCase):
    def test_ask_view(self):
        client = Client()
        response = client.get(reverse('ask'))
        self.assertEqual(response.status_code, 302)  # Код перенаправления 302 для успешного перенаправления
        self.assertRedirects(response, reverse('login') + '?continue=' + reverse('ask'))

