from django.db import models
from django.conf import settings
from django.db.models import Sum


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, default='avatar.png', upload_to='avatar/%Y/%m/%d')
    login = models.CharField(max_length=30)



class Tag(models.Model):
    tag = models.CharField(max_length=20)


class QuestionManager(models.Manager):
    def new_questions_list(self):
        return self.order_by('date').reverse()

    def hot_questions_list(self):
        return self.annotate(total_rating=Sum('questionrating__mark')).order_by('-total_rating')

    def find_by_tag(self, tag_name):
        return self.prefetch_related('tags').filter(tags__tag=tag_name)


class Question(models.Model):
    def rating_count(self):
        r_sum = QuestionRating.objects.filter(post=self).aggregate(Sum('mark'))
        return r_sum['mark__sum']

    def get_tags(self):
        tag_list = self.tags.all()
        tags = []
        for i in range(len(tag_list)):
            tags.append(tag_list[i].tag)
        return tags

    def answers_count(self):
        return Answer.objects.list_answers_count(self.pk)

    def get_negative_votes(self):
        votes = QuestionRating.objects.search_by_mark(self.pk, -1)
        users = []
        for vote in votes:
            users.append(vote.profile)
        return users

    def get_positive_votes(self):
        votes = QuestionRating.objects.search_by_mark(self.pk, 1)
        users = []
        for vote in votes:
            users.append(vote.profile)
        return users

    title = models.CharField(max_length=256)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    date = models.DateTimeField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    objects = QuestionManager()


class AnswerManager(models.Manager):
    def list_answers_count(self, question_id):
        return self.filter(question=question_id).count()

    def answers_list(self, question_id):
        return self.filter(question=question_id).annotate(total_rating=Sum('answerrating__mark')).order_by(
            '-total_rating')


class Answer(models.Model):
    def rating_count(self):
        r_sum = AnswerRating.objects.filter(post=self).aggregate(Sum('mark'))
        return r_sum['mark__sum']

    def get_negative_votes(self):
        votes = AnswerRating.objects.search_by_mark(self.pk, -1)
        users = []
        for vote in votes:
            users.append(vote.profile)
        return users

    def get_positive_votes(self):
        votes = AnswerRating.objects.search_by_mark(self.pk, 1)
        users = []
        for vote in votes:
            users.append(vote.profile)
        return users

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_correct = models.BooleanField(null=True)

    objects = AnswerManager()


class QuestionRatingManager(models.Manager):
    def search(self, question_id, profile_id):
        return self.filter(post=question_id, profile=profile_id).first()

    def search_by_mark(self, question_id, mark):
        return self.filter(post=question_id, mark=mark)


class QuestionRating(models.Model):
    mark = models.IntegerField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = QuestionRatingManager()


class AnswerRatingManager(models.Manager):
    def search(self, answer_id, profile_id):
        return self.filter(post=answer_id, profile=profile_id).first()

    def search_by_mark(self, answer_id, mark):
        return self.filter(post=answer_id, mark=mark)


class AnswerRating(models.Model):
    mark = models.IntegerField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Answer, on_delete=models.CASCADE)

    objects = AnswerRatingManager()
