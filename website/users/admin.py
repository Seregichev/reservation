# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext_lazy as _
from .models import Company, CustomUser
from weekday_field import fields as weekday_field
from weekday_field.widgets import ToggleCheckboxes

class CustomUserChangeForm(UserChangeForm):
    u"""Обеспечивает правильный функционал для поля с паролем и показ полей профиля."""
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    def clean_password(self):
        return self.initial["password"]

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    list_display = ('company', 'username', 'last_name', 'first_name', 'email',
                    'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
                'first_name', 'last_name', 'email', 'phone_number', 'company'
            )}),
        (_('Work time info'), {'fields': ('weekdays',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (None, {'fields': ('groups',)}),
        (None, {'fields': ('avatar',)}),
    )

    formfield_overrides = {
        weekday_field.WeekdayField: {'widget': ToggleCheckboxes},
    }


admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)


class CompanyAdmin (admin.ModelAdmin):

    list_display = [field.name for field in Company._meta.fields]

    class Meta:
        model = Company


admin.site.register(Company, CompanyAdmin)
