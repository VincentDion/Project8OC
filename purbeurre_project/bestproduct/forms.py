from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

"""On crée une nouvelle classe qui hérite de UserCreationForm à laquelle on rajoute un champ email,
c'est cette nouvelle classe que l'on appelle dans la view register"""

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']