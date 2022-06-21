from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from matplotlib import widgets
from . import models

# class ContactusForm(forms.Form):
#     Name = forms.CharField(max_length=30)
#     Enrollment = forms.CharField(max_length=40)
#     Email = forms.EmailField()
#     Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
#     Answer = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class ContactusForm(forms.ModelForm):
     class Meta:
        model=models.Contact
        fields=['name','enrollment','email','message','answer']
        widgets = {
            'message':forms.Textarea(attrs={'rows': 3, 'cols': 30}),
            'answer':forms.Textarea(attrs={'rows': 3, 'cols': 30})
        }


class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']



class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['enrollment','branch']

class BookForm(forms.ModelForm):
    class Meta:
        model=models.Book
        fields=['name','isbn','author','category']

class IssuedBookFormEdit(forms.ModelForm):
    class Meta:
        model = models.IssuedBook
        fields=['enrollment','isbn','issuedate','expirydate']

class IssuedBookForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of book model will be shown there in html
    isbn2=forms.ModelChoiceField(queryset=models.Book.objects.all(),empty_label="Name and isbn", to_field_name="isbn",label='Name and Isbn')
    enrollment2=forms.ModelChoiceField(queryset=models.StudentExtra.objects.all(),empty_label="Name and enrollment",to_field_name='enrollment',label='Name and enrollment')
    
