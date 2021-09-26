from .models import Person, Sponsor
from django import forms
from django.forms import  ModelForm


class BioForm(ModelForm):

    class Meta:
        model=Person
        fields=('first_name','last_name','address','phone','email')


class SchoolForm(ModelForm):

    class Meta:
        model=Person
        fields=('schoolName','schoolAddress','academic_level', 'expected_year_of_completion')

        
class RecommendationForm(ModelForm):

    class Meta:
        model=Person
        fields=('reasons','recommendation_letter')