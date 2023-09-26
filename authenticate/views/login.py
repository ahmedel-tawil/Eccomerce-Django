import requests
from django.template import RequestContext
from company.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from home.context_processors import get_location, get_ip, get_currency_code


def SignInView(request):
    ''' Sign in views '''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email).first()
        if user is None:
            messages.info(request, '%s Not found!' % email)
            return redirect('sign-in')

        profile = User.objects.filter(email=user).first()
        ''' User verification checks '''
        if not profile.is_verified:
            messages.info(request, 'Your account is not verified!')
            # Resend verification email
            return redirect('sign-in')

        auth_user = authenticate(email=email, password=password)
        if auth_user is None:
            messages.info(request, 'Wrong credentials')
            return redirect('sign-in')
        login(request, auth_user)
        currency_session = get_currency_code()
        # messages.info(request, f'Currency will Be displayed as {currency_session}')
        # request.session['currency'] = user.currency.code
        request.session['currency'] = currency_session

        return redirect('landing')
    return render(request, 'authenticate/LogIn.html', )
