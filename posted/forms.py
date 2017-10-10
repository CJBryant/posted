from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationForm
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field
from crispy_forms.bootstrap import StrictButton, FormActions

class MyRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super(MyRegistrationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.helper = FormHelper()
        self.helper.form_class = 'form-accounts'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Fieldset(
                'Sign up',
                Field('username', name='username', placeholder='Username', autofocus=''),
                Field('email', name='email', placeholder='Email'),
                Field('password1', name='password1', placeholder='Password'),
                Field('password2', name='password2', placeholder='Password (again)'),
            ),
            FormActions(
                StrictButton('Register', css_class='btn btn-lg btn-primary btn-block register-btn', type='submit')
            ),
        )

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput)
    #remember_me = forms.BooleanField(required=False, help_text='Remember me', widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-accounts'
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Fieldset(
                'Please sign in',
                Field('username', name='username', placeholder='Username', autofocus=''),
                Field('password', name='password', placeholder='Password'),
                #Field('remember_me', value='remember-me')
            ),
            FormActions(
                StrictButton('Sign in', css_class='btn btn-lg btn-primary btn-block login', type='submit')
            ),
        )
