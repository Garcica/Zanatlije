from django.forms import forms, CharField


class LoginForm(forms.Form):
    keyword = CharField(max_length=50)
