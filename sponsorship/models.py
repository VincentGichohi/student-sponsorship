from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff,
        is_active=True,
        is_sponsor=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    return user

  def create_sponsor(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_admin=models.BooleanField(default=False)
    is_sponsor=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/sponsorship/%i/" % (self.pk)


class Student(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
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
    sponsorEmail=models.EmailField(default=None, unique=True)
    country=models.CharField(max_length=200)
    sponsoredSchool=models.CharField(max_length=200)
    type_of_sponsorship=models.TextField(default=None)

    def __str__(self):
        return self.sponsorName
    