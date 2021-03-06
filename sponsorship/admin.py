from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Sponsor, MyUser, Applications
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from .forms import RegistrationForm, CustomUserChangeForm, RegistrationForm

admin.site.register(Student)
admin.site.register(Sponsor)
admin.site.register(Applications)
# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = RegistrationForm
    form = CustomUserChangeForm
    model = MyUser
    list_display = ('email', 'is_staff', 'is_active','is_superuser','is_sponsor')
    list_filter = ('email', 'is_staff', 'is_active','is_superuser','is_sponsor')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser','is_sponsor', 'is_student',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','is_superuser','is_sponsor')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

User = get_user_model
admin.site.register(MyUser, CustomUserAdmin)
