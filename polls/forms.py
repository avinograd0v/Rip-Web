from django.contrib.auth.models import User
from .models import Profile, Answer, Question
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

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