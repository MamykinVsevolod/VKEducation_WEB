from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
import re

from app.models import Profile, Question, Tag, Answer, QuestionRating, AnswerRating


class LoginForm(forms.Form):
    login = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'InputLogin', 'placeholder': 'Логин для входа в систему'}),
        max_length=30,
        label='Введите логин:')
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'id': 'InputPassword', 'placeholder': 'Пароль от аккаунта'}), max_length=30,
        min_length=6, label='Введите пароль:')

    def clean_password(self):
        password = self.cleaned_data['password']
        if password is None:
            raise ValidationError('Пожалуйста, введите пароль.')
        return password

    def clean_login(self):
        login = self.cleaned_data['login']
        if login is None:
            raise ValidationError('Пожалуйста, введите логин.')
        return login


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputLogin',
                                      'placeholder': 'Логин для входа в аккаунт'}),
        max_length=15,
        label='Логин', required=True)
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'InputEmail', 'placeholder': 'Адрес электронной почты'}),
        max_length=40,
        label='Эл. почта', required=True, help_text='Формат почты: example@example.com')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'InputPassword'}), max_length=30, min_length=6,
        label='Пароль', required=True, help_text='Минимальная длина пароля - 6 символов.')
    password_check = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'InputPasswordAgain'}), max_length=30,
        min_length=6,
        label='Повторите пароль', required=True)
    nickname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputNickname',
                                      'placeholder': 'Отображаемое имя'}),
        max_length=30,
        label='Никнейм', required=True)
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'InputAvatar'}),
                              label='Загрузите аватар', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        if password != password_check:
            self.add_error('password_check', 'Введенные пароли не совпадают.')
            raise ValidationError('Введенные пароли не совпадают.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if re.fullmatch(r'(\d|\w|_|-|\.)*', username):
            return username
        else:
            self.add_error(None,
                           'В логине обнаружены недопустимые символы.')
            raise ValidationError(self)

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if re.fullmatch(r'(\d|\w|_|-|\.)*', nickname):
            return nickname
        else:
            self.add_error(None,
                           'В имени пользователя обнаружены недопустимые символы.')
            raise ValidationError(self)

    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        nickname = self.cleaned_data['nickname']
        avatar = self.cleaned_data['avatar']

        user_profile = Profile(login=nickname, user=user)
        if avatar is not None:
            user_profile.avatar = avatar
        user_profile.save()
        return user


class QuestionForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputTitle',
                                      'placeholder': 'Заголовок вашего вопроса'}), max_length=70, min_length=10,
        label='Заголовок вопроса', required=True)
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'InputText',
                                     'placeholder': 'Опишите вашу проблему'}), max_length=1000, min_length=50,
        label='Текст', required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputTags',
                                                         'placeholder': 'Ключевые слова, относящиеся к теме вопроса'}),
                           max_length=50,
                           label='Теги', required=True, help_text='Максимальное количество тегов: 3')

    class Meta:
        model = Question
        fields = ['title', 'text']

    def get_tags(self, tags):
        saved_tags = []
        for tag in tags:
            tag_obj = Tag.objects.filter(tag=tag).first()
            if tag_obj is None:
                tag_obj = Tag.objects.create(tag=tag)
            saved_tags.append(tag_obj)
        return saved_tags

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if not re.fullmatch(r'(\w|,| |;)*', tags):
            self.add_error(None, 'В списке тегов обнаружены недопустимые символы.')
            raise ValidationError(self)
        tags = re.split(', |; | ', tags)
        if len(tags) > 3:
            self.add_error(None, 'Вы не можете ввести больше трех тегов.')
            raise ValidationError(self)
        tags = self.get_tags(tags)
        return tags

    def save(self, request, **kwargs):
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        tags = self.cleaned_data['tags']
        date = datetime.now()
        profile = request.user.profile

        question = Question(title=title, text=text, date=date, profile=profile)
        question.save()
        question.tags.add(*tags)
        QuestionRating.objects.create(post=question, mark=0)
        return question


class AnswerForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control border-secondary', 'id': 'InputText',
                                     'placeholder': 'Введите текст ответа', 'rows': 5}), max_length=2000, min_length=10,
        label='Добавьте свой ответ:', required=True)

    class Meta:
        model = Answer
        fields = ['text']

    def save(self, request, question_id, **kwargs):
        text = self.cleaned_data['text']
        date = datetime.now()
        profile = request.user.profile
        question = Question.objects.filter(pk=question_id).first()

        answer = Answer(text=text, date=date, profile=profile, question=question, is_correct=None)
        answer.save()
        AnswerRating.objects.create(post=answer, mark=0)
        return answer


class SettingsForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputLogin'}), max_length=15,
        label='Логин')
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputEmail'}), max_length=40,
        label='Эл. почта')
    nickname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputNickname'}), max_length=30,
        label='Никнейм')
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'InputAvatar'}), label='Аватар',
        required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if re.fullmatch(r'(\d|\w|_|-|\.)*', username):
            return username
        else:
            self.add_error(None,
                           'В логине обнаружены недопустимые символы.')
            raise ValidationError(self)

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if re.fullmatch(r'(\d|\w|_|-|\.)*', nickname):
            return nickname
        else:
            self.add_error(None,
                           'В имени пользователя обнаружены недопустимые символы.')
            raise ValidationError(self)

    def save(self, request, **kwargs):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        user = request.user
        user.username = username
        user.email = email
        profile = request.user.profile
        nickname = self.cleaned_data['nickname']
        avatar = self.cleaned_data['avatar']
        profile.login = nickname
        if avatar is not None:
            profile.avatar = avatar
        profile.save()
        user.save()
