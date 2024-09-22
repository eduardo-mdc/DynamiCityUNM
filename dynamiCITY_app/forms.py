from django import forms
from django.contrib.auth.forms import AuthenticationForm

class MDBAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label='Remember Me', required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super(MDBAuthenticationForm,self).__init__(*args, **kwargs)
        # Apply MDB Bootstrap classes to form fields
        for field in self.fields.values():
            if field.label == 'Remember Me':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control form-control-lg'

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', max_length=30, widget=forms.PasswordInput)
    is_admin = forms.BooleanField(label='Admin', required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'is_admin':
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control'
            


class EditForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=30, required=False, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', required=False,max_length=30, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'