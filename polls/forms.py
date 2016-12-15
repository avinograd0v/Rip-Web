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
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter tags, divided by commas',
                                                         'autocomplete': 'off'}))

    def __init__(self, *args, **kwargs):
        super(QuestionCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['header', 'content']


class MyUserChangeForm(UserChangeForm):
    #password = forms.CharField(widget=forms.PasswordInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    #def clean_password(self):
    #    password = self.cleaned_data['password']
    #    return password

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


