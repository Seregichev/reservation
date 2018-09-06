# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, logout


def login_view(request):
    login_form = LoginForm(request.POST or None)

    if request.user.is_authenticated():

        return redirect('/')

    else:
        if request.POST and login_form.is_valid():
            user = login_form.login(request)
            if user:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'users/auth/login.html', {'login_form': login_form, })


def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))