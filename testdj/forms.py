


from django import forms
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"uusername",
        error_messages={'required': 'input name'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"username",
            }
        ),
    )    
    password = forms.CharField(
        required=True,
        label=u"passwd",
        error_messages={'required': u'input passwd'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"passwd",
            }
        ),
    )   
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"input must")
        else:
            cleaned_data = super(LoginForm, self).clean() 
