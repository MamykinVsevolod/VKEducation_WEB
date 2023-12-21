import os

import django
#from .askme import settings
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askme.settings')
#django.setup()
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from faker import Faker

from app.models import Profile, Tag, Question, Answer, QuestionRating, AnswerRating


fake = Faker()


class Command(BaseCommand):
    help = 'Filling Database'

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **kwargs):
        num = kwargs['num']
        rate = int(num / 100)

        users = [
            User(
                username=fake.unique.user_name()[:fake.random_int(min=3, max=8)] + fake.unique.user_name()[
                                                                                   :fake.random_int(min=3,
                                                                                                    max=7)] + f'{fake.random_int(min=0, max=1000)}',
                email=fake.email(),
                password=fake.password(special_chars=False),
                first_name=fake.first_name(),
                last_name=fake.last_name()
            ) for i in range(num)
        ]
        User.objects.bulk_create(users)
        self.stdout.write("Finished with users")
        users = User.objects.all()

        profiles = [
            Profile(
                user=users[i],
                login=fake.first_name() + '_' + fake.last_name()
            ) for i in range(num)
        ]
        Profile.objects.bulk_create(profiles)
        self.stdout.write("Finished with profiles")
        profiles = Profile.objects.all()

        _tags = [
            Tag(
                tag=fake.word()
            ) for _ in range(num)
        ]
        Tag.objects.bulk_create(_tags)
        self.stdout.write("Finished with tags")
        _tags = Tag.objects.all()

        questions = [
            Question(
                title=fake.sentence(nb_words=fake.random_int(min=2, max=7)),
                text=fake.text(max_nb_chars=200),
                date=str(fake.date_time_this_decade()),
                profile=profiles[fake.random_int(min=0, max=num - 1)]
            ) for i in range(num * 10)
        ]
        Question.objects.bulk_create(questions)
        questions = Question.objects.all()
        for q in questions:
            q.tags.set([_tags[fake.random_int(min=0, max=num - 1)] for _ in range(fake.random_int(min=1, max=3))])
        self.stdout.write("Finished with questions")

        answers = [
            Answer(
                question=questions[fake.random_int(min=0, max=num * 10 - 1)],
                text=fake.text(max_nb_chars=500),
                date=str(fake.date_time_this_decade()),
                profile=profiles[fake.random_int(min=0, max=num - 1)],
                is_correct=True if (fake.random_int() % 10 == 0) else (False if (fake.random_int() % 5 != 0) else None),
            ) for i in range(num * 100)
        ]
        Answer.objects.bulk_create(answers)
        self.stdout.write("Finished with answers")
        answers = Answer.objects.all()







        question_ratings = [
            QuestionRating(
                mark=-1 if fake.random_int(min=0, max=100) % 4 == 0 else 1,
                profile=profiles[fake.random_int(min=0, max=num - 1)],
                post=questions[i] if i < num * 10 else questions[fake.random_int(min=0, max=10 * num - 1)]
            ) for i in range(num * 10 * rate)
        ]
        QuestionRating.objects.bulk_create(question_ratings)
        self.stdout.write("Finished with Question ratings")






        # question_range = min(num * 10, len(questions))  # Определяем правильный диапазон выбора вопросов
        #
        # question_ratings = [
        #     QuestionRating(
        #         mark=-1 if fake.random_int(min=0, max=100) % 4 == 0 else 1,
        #         profile=profiles[fake.random_int(min=0, max=num - 1)],
        #         post=questions[i % question_range]  # Используем операцию модуля для выбора вопроса
        #     ) for i in range(num * 10 * rate)
        # ]


        answer_ratings = [
            AnswerRating(
                mark=-1 if fake.random_int(min=0, max=100) % 4 == 0 else 1,
                profile=profiles[fake.random_int(min=0, max=num - 1)],
                post=answers[i] if i < num * 100 else answers[fake.random_int(min=0, max=100 * num - 1)]
            ) for i in range(num * 100 * 10) # вместо * 10 в конце было * rate
        ]
        AnswerRating.objects.bulk_create(answer_ratings)
        self.stdout.write("Finished with Answer ratings")
        answers = Answer.objects.all()
        profiles = Profile.objects.all()
        for i in range(1_000_000):
            rating = AnswerRating.objects.create(mark=-1 if i % 4 == 0 else 1, post=answers[i],
                                                 profile=profiles[fake.random_int(min=0, max=num - 1)])
            self.stdout.write(str(rating.pk))