from django.contrib import admin

# Register your models here.
from .models import Profile, Tag, Question, Answer, QuestionRating, AnswerRating

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionRating)
admin.site.register(AnswerRating)