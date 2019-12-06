from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

"""We create a new class inheriting from UserCreationForm to which we had an email field,
it is this new class we call in the register view"""

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ChangeMailForm(forms.Form):
	email = forms.EmailField(label='Your new email')

# https://docs.djangoproject.com/fr/2.1/ref/forms/api/#django.forms.Form.cleaned_data