from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from app.models import Profile, Question, Tag, Answer, QuestionRating, AnswerRating


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.profile = Profile.objects.create(login='test_user', user=self.user)

    def test_profile_creation(self):
        self.assertEqual(self.profile.login, 'test_user')


class QuestionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.profile = Profile.objects.create(login='test_user', user=self.user)
        self.question = Question.objects.create(title='Test Question', text='This is a test question',
                                                date=timezone.now(), profile=self.profile)

    def test_question_creation(self):
        self.assertEqual(self.question.title, 'Test Question')
        self.assertEqual(self.question.text, 'This is a test question')


class QuestionTagsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.profile = Profile.objects.create(login='test_user', user=self.user)
        self.tag1 = Tag.objects.create(tag='tag1')
        self.tag2 = Tag.objects.create(tag='tag2')
        self.question = Question.objects.create(title='Test Question', text='This is a test question',
                                                date=timezone.now(), profile=self.profile)
        self.question.tags.add(self.tag1, self.tag2)

    def test_question_tags(self):
        self.assertEqual(self.question.tags.count(), 2)
        self.assertIn(self.tag1, self.question.tags.all())
        self.assertIn(self.tag2, self.question.tags.all())


class AnswerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.profile = Profile.objects.create(login='test_user', user=self.user)
        self.question = Question.objects.create(title='Test Question', text='This is a test question',
                                                date=timezone.now(), profile=self.profile)
        self.answer1 = Answer.objects.create(question=self.question, text='Answer 1', date=timezone.now(),
                                             profile=self.profile)
        self.answer2 = Answer.objects.create(question=self.question, text='Answer 2', date=timezone.now(),
                                             profile=self.profile)

    def test_question_answers(self):
        self.assertEqual(self.question.answers_count(), 2)
        self.assertIn(self.answer1, self.question.answer_set.all())
        self.assertIn(self.answer2, self.question.answer_set.all())


class QuestionRatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.profile = Profile.objects.create(login='test_user', user=self.user)
        self.question = Question.objects.create(title='Test Question', text='This is a test question',
                                                date=timezone.now(), profile=self.profile)
        QuestionRating.objects.create(mark=1, profile=self.profile, post=self.question)
        QuestionRating.objects.create(mark=-1, profile=self.profile, post=self.question)

    def test_question_rating(self):
        self.assertEqual(self.question.rating_count(), 0)


class AnswerRatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.profile = Profile.objects.create(login='test_user', user=self.user)
        self.question = Question.objects.create(title='Test Question', text='This is a test question',
                                                date=timezone.now(), profile=self.profile)
        self.answer = Answer.objects.create(question=self.question, text='Test Answer', date=timezone.now(),
                                            profile=self.profile)
        AnswerRating.objects.create(mark=1, profile=self.profile, post=self.answer)
        AnswerRating.objects.create(mark=-1, profile=self.profile, post=self.answer)

    def test_answer_rating(self):
        self.assertEqual(self.answer.rating_count(), 0)
