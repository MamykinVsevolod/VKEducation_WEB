from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app import views


class UrlsTest(SimpleTestCase):
    def test_start_url_resolves(self):
        url = reverse('start')
        self.assertEqual(resolve(url).func, views.index)

    def test_index_url_resolves(self):
        url = reverse('index', args=[1])
        self.assertEqual(resolve(url).func, views.index)

    def test_hot_url_resolves(self):
        url = reverse('hot', args=[1])
        self.assertEqual(resolve(url).func, views.hot)

    def test_tag_url_resolves(self):
        url = reverse('tag', args=['example_tag', 1])
        self.assertEqual(resolve(url).func, views.tag)

    def test_question_url_resolves(self):
        url = reverse('question', args=[1, 1])
        self.assertEqual(resolve(url).func, views.question)

    def test_ask_url_resolves(self):
        url = reverse('ask')
        self.assertEqual(resolve(url).func, views.ask)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.log_in)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.logout)

    def test_settings_url_resolves(self):
        url = reverse('settings')
        self.assertEqual(resolve(url).func, views.settings)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, views.signup)

    def test_rate_url_resolves(self):
        url = reverse('rate')
        self.assertEqual(resolve(url).func, views.rate)

    def test_correct_url_resolves(self):
        url = reverse('correct')
        self.assertEqual(resolve(url).func, views.correct)

    def test_admin_url_resolves(self):
        url = reverse('admin:index')
        self.assertEqual(resolve(url).route, 'admin/')
        self.assertEqual(resolve(url).app_name, 'admin')
