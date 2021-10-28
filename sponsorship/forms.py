from .models import Student, Sponsor
from django import forms
from django.forms import  ModelForm, fields
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class RegistrationForm(UserCreationForm):
    """
      Form for Registering new users 
    """
    email = forms.EmailField(max_length=60, help_text = 'Required. Add a valid email address')
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
          specifying styles to fields 
        """
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in (self.fields['email'],self.fields['password1'],self.fields['password2']):
            field.widget.attrs.update({'class': 'form-control '})
    # class Meta:
    #     model = CustomUser
    #     fields = ('email',)

class AccountAuthenticationForm(forms.ModelForm):
    """
      Form for Logging in  users
    """
    password  = forms.CharField(label= 'Password', widget=forms.PasswordInput)

    class Meta:
        model  =  User
        fields =  ('email', 'password')
        widgets = {
                   'email':forms.TextInput(attrs={'class':'form-control'}),
                   'password':forms.TextInput(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        """
          specifying styles to fields 
        """
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        for field in (self.fields['email'],self.fields['password']):
            field.widget.attrs.update({'class': 'form-control '})

    def clean(self):
        if self.is_valid():

            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')

class AccountUpdateform(forms.ModelForm):
    """
      Updating User Info
    """
    class Meta:
        model  = User
        fields = ('email',)
        widgets = {
                   'email':forms.TextInput(attrs={'class':'form-control'}),
                   'password':forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """
          specifying styles to fields 
        """
        super(AccountUpdateform, self).__init__(*args, **kwargs)
        for field in (self.fields['email']):
            field.widget.attrs.update({'class': 'form-control '})

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = CustomUser.objects.exclude(pk = self.instance.pk).get(email=email)
            except CustomUser.DoesNotExist:
                return email
            raise forms.ValidationError("Email '%s' already in use." %email)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

class ContactForm(forms.Form):
	first_name = forms.CharField(max_length = 50)
	last_name = forms.CharField(max_length = 50)
	email_address = forms.EmailField(max_length = 150)
	message = forms.CharField(widget = forms.Textarea, max_length = 2000)

class StudentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields= ('email', 'is_student')

    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_student=True
        user.save()
        student=Student.objects.create(user=user)
        return user
class SponsorSignUpForm(UserCreationForm):
    model = User
    fields = ('email', 'is_sponsor')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_sponsor= True
        user.save()
        sponsor= Sponsor.objects.create(user=user)
        return user
class StaffSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email','is_staff')

    def save(self, commit = True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user

#a form for updating Bio information
class BioForm(ModelForm):

    class Meta:
        model=Student
        fields=('first_name',
        'last_name','address',
        'phone','email',
        'birth_certificate',
        'national_id_file',
        )
#a form for updating School information
class SchoolForm(ModelForm):

    class Meta:
        model = Student
        fields = (
            'school_name','school_address','academic_level','expected_year_of_completion'
        )
#a form for updating Recommendation and reasons
class RecommendationForm(ModelForm):

    class Meta:
        model= Student
        fields = (
            'reasons_for_sponsorship','recommendation_letter'
        )

class Success(forms.Form):
    Email=forms.EmailField()

    def __str__(self):
        return self.Email


# class SchoolForm(ModelForm):
#
#     class Meta:
#         model=Student
#         fields=('school_name','school_address','academic_level','expected_year_of_completion')
#
#
# class RecommendationForm(ModelForm):
#
#     class Meta:
#         model=Student
#         fields=('reasons_for_sponsorship','recommendation_letter')

class SponsorForm(forms.Form):

    class Meta:
        model=Sponsor
        fields=(
            'sponsorName','country_of_origin','sponsoredSchool','type_of_sponsorship'
        )