
from django import forms
from django.contrib.auth import get_user_model
from django.forms.models import ModelFormMetaclass

class CustomMetaClass(ModelFormMetaclass):
    def __new__(cls,bases,*args,**kwargs):
       args[1].get('Meta').fields=args[1].get('Meta').update_fields
       return super().__new__(cls,bases,*args,**kwargs)

class UserForm(forms.ModelForm,metaclass=CustomMetaClass):
    class Meta:
        model=get_user_model()
        fields=("username",'email',"password")
        update_fields=("username","email")
        
    
    def save(self, commit = ...):
        
        return super().save(commit=True)
    
