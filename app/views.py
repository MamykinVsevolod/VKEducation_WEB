# Create your views here.
import json

from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError

from .forms import LoginForm, RegisterForm, QuestionForm, SettingsForm, AnswerForm
from .models import Question, Answer, QuestionRating, AnswerRating
# QUESTIONS = [
#     {
#         'id': i,
#         'title': f'Вопрос {i}',
#         'content': 'VK — это более 200 проектов и сервисов, которыми пользуются миллионы. Ты можешь присоединиться к команде, которая их создаёт. Познакомься с нашим офисом и посети виртуальную экскурсию.'
#     } for i in range(100)
# ]
#
# ANSWERS = [
#     {
#         'content': 'VK — это более 200 проектов и сервисов, которыми пользуются миллионы. Ты можешь присоединиться к команде, которая их создаёт. Познакомься с нашим офисом и посети виртуальную экскурсию.'
#     } for i in range(100)
# ]
#
# HOT_QUESTIONS = [
#     {
#         'id': i,
#         'title': f'Вопрос {i * i}',
#         'content': 'VK — это более 200 проектов и сервисов, которыми пользуются миллионы. Ты можешь присоединиться к команде, которая их создаёт. Познакомься с нашим офисом и посети виртуальную экскурсию.'
#     } for i in range(20)
# ]
#
# TAG_QUESTIONS = [
#     {
#         'id': i,
#         'title': f'Вопрос {i}',
#         'content': 'VK — это более 200 проектов и сервисов, которыми пользуются миллионы. Ты можешь присоединиться к команде, которая их создаёт. Познакомься с нашим офисом и посети виртуальную экскурсию.'
#     } for i in range(20)
# ]


def paginate(objects, page, per_page=5):
    paginator = Paginator(objects, per_page)
    obj = paginator.get_page(page)
    # page_items = paginator.page(1).object_list
    """ return paginator.page(page) """
    return obj


def get_paginator(objects, per_page=5):
    paginator = Paginator(objects, per_page)
    return paginator


def index(request, page=1):
    questions = Question.objects.new_questions_list()
    # paginator = Paginator(QUESTIONS, 3)
    # page_items = paginator.page(1).object_list
    """return render(request, 'index.html', {'questions': paginate(QUESTIONS, page), page: page})"""
    return render(request, 'index.html',
                  {'items': paginate(questions, page), 'paginator': get_paginator(questions)})


def hot(request, page=1):
    questions = Question.objects.hot_questions_list()
    return render(request, 'hot.html',
                  {'items': paginate(questions, page), 'paginator': get_paginator(questions)})


def tag(request, tag_name, page=1):
    questions = Question.objects.find_by_tag(tag_name)
    # paginator = Paginator(QUESTIONS, 3)
    # page_items = paginator.page(1).object_list
    """return render(request, 'index.html', {'questions': paginate(QUESTIONS, page), page: page})"""
    return render(request, 'tag.html', {'tag': tag_name, 'items': paginate(questions, page),
                                        'paginator': get_paginator(questions)})

@csrf_protect
def question(request, question_id, page=1):
    if request.method == "GET":
        answer_form = AnswerForm()
    elif request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(request, question_id)
            return redirect(reverse('question', kwargs={'question_id': question_id, 'page': 1}) + f'#{answer.pk}')
    item = get_object_or_404(Question.objects.all(), pk=question_id)
    answers = Answer.objects.answers_list(question_id)
    return render(request, 'question.html',
                  {'item': item, 'items': paginate(answers, page), 'paginator': get_paginator(answers), 'form': answer_form})


def ask(request):
    return render(request, 'ask.html')

@csrf_protect
def log_in(request):
    if request.user.is_authenticated:
        return redirect(reverse('start'))
    if request.method == "GET":
        login_form = LoginForm()
    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.clean_login()
            password = login_form.clean_password()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('continue') is not None:
                    if request.GET.get('continue') == '/login' or request.GET.get('continue') == '/signup':
                        return redirect(reverse('start'))
                    return redirect(request.GET.get('continue'))
                else:
                    return redirect(reverse('start'))
            else:
                login_form.add_error(None, "Неверное имя пользователя или пароль.")
    return render(request, 'login.html', context={'form': login_form})


def settings(request):
    return render(request, 'settings.html')

@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('start'))

    if request.method == "GET":
        signup_form = RegisterForm()
    elif request.method == "POST":
        signup_form = RegisterForm(request.POST, request.FILES)
        if signup_form.is_valid():
            try:
                user = signup_form.save()
                login(request, user)
                if request.GET.get('continue') is not None:
                    if request.GET.get('continue') == '/login' or request.GET.get('continue') == '/signup':
                        return redirect(reverse('start'))
                    return redirect(request.GET.get('continue'))
                else:
                    return redirect(reverse('start'))
            except IntegrityError:
                signup_form.add_error(None, 'Пользователь с таким именем уже существует.')
    return render(request, 'signup.html', context={'form': signup_form})


@login_required(login_url='login', redirect_field_name='continue')
def logout(request):
    auth.logout(request)
    if request.GET.get('continue') is not None:
        if request.GET.get('continue') == '/login' or request.GET.get('continue') == '/signup':
            return redirect(reverse('start'))
        return redirect(request.GET.get('continue'))
    else:
        return redirect(reverse('start'))
