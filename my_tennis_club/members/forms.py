from django import forms

class MemberForm(forms.Form):
    firstname = forms.CharField(max_length=50)
    lastname = forms.CharField(max_length=50)
    phone = forms.IntegerField(required=False)
    joined_date = forms.DateField(required=False)
