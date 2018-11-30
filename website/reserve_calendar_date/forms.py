# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from .models import Reservation


class ContactForm (forms.Form):

    name = forms.CharField(required=True, label=_('Name'), max_length=256,
                           help_text=_('Write your name. Example: Victor'),
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'type': 'text'}),
                            )

    email = forms.EmailField(required=False, label=_('Emаil'), min_length=5, max_length=256,
                             help_text=_('Write your email adress. Example: myemail@example.com'),
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'type': 'email'}),
                            )

    phone_number = forms.RegexField(required=False, label=_('Phone'), regex=r'^\+?1?\d{9,15}$', max_length=64,
                                    help_text=_('Write your phone number. Example: +79991234567'),
                                    error_messages={
                                        'invalid':_("Phone number must be entered in the format: '+79999999999'. Up to 15 digits allowed.")},
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control',
                                               'type': 'tel'}),
                                    )
    comment = forms.CharField(required=False, label=_('Comment'), max_length=256,
                              help_text=_('Write your comment. Example: I want to pay cash.'),
                              widget=forms.Textarea(
                                  attrs={'class': 'form-control', 'rows': '3'}),
                              )



    # def clean(self):
    #     if not self._errors:
    #         cleaned_data = super(ContactForm, self).clean()
    #         username = cleaned_data.get('username')
    #         password = cleaned_data.get('password')
    #         try:
    #             user = User.objects.get(username=username)
    #             if not user.check_password(password):
    #                 raise forms.ValidationError(u'Неверное сочетание e-mail \ Пароль.')
    #             elif not user.is_active:
    #                 raise forms.ValidationError(u'Пользователь с таким e-mail заблокирован.')
    #         except User.DoesNotExist:
    #             raise forms.ValidationError(u'Пользователь с таким Логином не существует.')
    #         return cleaned_data

    # def login(self, request):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     user = authenticate(username=username, password=password)
    #     return user

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['master', 'client', 'client_name', 'client_email', 'client_phone', 'start_time', 'end_time', 'product', 'price', 'comment', 'status']


class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['status']

class DetailForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['master', 'client', 'client_name', 'client_email', 'client_phone', 'start_time', 'end_time', 'product', 'price', 'comment']
