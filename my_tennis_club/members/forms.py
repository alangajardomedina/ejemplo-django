from django import forms

class MemberForm(forms.Form):
    firstname = forms.CharField(max_length=50)
    lastname = forms.CharField(max_length=50)
    phone = forms.IntegerField(required=False)
    joined_date = forms.DateField(required=False)
    email = forms.EmailField()
    password = forms.CharField(max_length=16)
    repeat_password = forms.CharField(max_length=16)
    tipo_usuario = forms.CharField(max_length=40)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=16)

class RegistroForm(forms.Form):
    firstname = forms.CharField(max_length=50)
    lastname = forms.CharField(max_length=50)
    phone = forms.IntegerField(required=False)
    joined_date = forms.DateField(required=False)
    email = forms.EmailField()
    password = forms.CharField(max_length=16)
    repeat_password = forms.CharField(max_length=16)
