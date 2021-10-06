from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_sponsor = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class StudentName(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)

class Student(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    full_names=models.ForeignKey(StudentName, on_delete=models.CASCADE)
    address=models.CharField(max_length=50)
    phone=models.IntegerField()
    email=models.EmailField(default=None, unique=True)
    birth_certificate=models.FileField(upload_to='images')
    national_id_file=models.FileField(upload_to='images')
    school_name=models.CharField(max_length=200)
    school_address=models.CharField(max_length=100)
    academic_level=models.TextField()
    expected_year_of_completion=models.DateField(default=None)
    reasons_for_sponsorship=models.TextField()
    recommendation_letter=models.FileField(upload_to='images')

    
    def __str__(self):
        return self.first_name

class Sponsor(models.Model):
    sponsorName=models.CharField(max_length=200)
    country_of_origin=models.CharField(max_length=200)
    sponsoredSchool=models.CharField(max_length=200)
    type_of_sponsorship=models.TextField(default=None)

    def __str__(self):
        return self.sponsorName
    
