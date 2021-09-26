from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
# Create your models here.
class Person(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    address=models.CharField(max_length=50)
    phone=models.IntegerField()
    email=models.EmailField(default=None, unique=True)
    birth_certificate=models.FileField(upload_to='images')
    national_id_file=models.FileField(upload_to='images')
    school_name=models.CharField(max_length=200)
    school_address=models.CharField(max_length=100)
    academic_level=models.TextField
    expected_year_of_completion=models.DateField(default=None)
    reasons_for_sponsorship=models.TextField(default=False)
    recommendation_letter=models.FileField(upload_to='images')

    
    def __str__(self):
        return self.first_name

class Sponsor(models.Model):
    sponsorName=models.CharField(max_length=200)
    SponsorEmail=models.EmailField(default=None, unique=True)
    country=models.CharField(max_length=200)
    sponsoredSchool=models.CharField(max_length=200)
    type_of_sponsorship=models.TextField(default=None)

    def __str__(self):
        return self.sponsorName
    