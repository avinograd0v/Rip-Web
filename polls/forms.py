from django.contrib.auth.models import User
from .models import Profile, Answer, Question
from django import forms
from django.contrib.auth.forms import UserChangeForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['header', 'content']

        widgets = {
            'content': forms.Textarea(
                attrs={'id': 'question-text', 'required': True}
            ),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

        widgets = {
            'content': forms.Textarea(
                attrs={'id': 'answer-text', 'required': True, 'placeholder': 'Answer...'}
            ),
        }


class QuestionCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionCreateForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs = {'class': 'selectpicker',
                                            'data-live-search': 'true',
                                            'data-live-search-normalize': 'true',
                                            'data-live-search-placeholder': 'Search tags...'}

    class Meta:
        model = Question
        fields = ['header', 'content', 'tags']


class MyUserChangeForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

