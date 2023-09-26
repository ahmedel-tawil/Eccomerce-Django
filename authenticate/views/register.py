import uuid
from authenticate.views.email_verify import sendVerifyToken
from company.models import User
from currencies.models import Currency
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.shortcuts import redirect, render
from home.context_processors import get_location, get_ip, get_currency_code


# from django.contrib.gis.utils import
def RegisterView(request):
    ''' Sign up new user to freshdesk '''
    ip = get_ip()
    currency_code = get_currency_code()
    assigned_currency = Currency.objects.get(code=currency_code)

    if request.method == 'POST':
        name = request.POST.get('name')
        # organization = request.POST.get('OrganizationName')
        mobile = request.POST.get('MobileNumber')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        repeatPassword = request.POST.get('RepeatPassword')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists.')
            return redirect('sign-up')
        if User.objects.filter(phone_number=mobile).exists():
            messages.info(request, 'Mobile number already exists.')
            return redirect('sign-up')

        if password and repeatPassword:
            if password != repeatPassword:
                messages.info(request, "The two password fields didn't match.")
                return redirect('sign-up')
        print('Passed all errors')
        with transaction.atomic():
            # If something went wrong/fails
            # The database will perform a rollback by itself.
            auth_token = str(uuid.uuid4())
            user_create = User.objects.create(name=name,
                                              phone_number=mobile,
                                              email=email,
                                              token=auth_token,
                                              ip_address=ip,
                                              currency=assigned_currency,
                                              )
            user_create.set_password(password)
            user_create.save()
            # to get the domain of the current site
            current_site = request.get_host()
            sendVerifyToken(email, auth_token, current_site)
            return redirect('token_send')
    return render(request, 'authenticate/register.html')


def Tokensend(request):
    '''Let user to check there email for further instruction '''
    return render(request, 'authenticate/token_send.html')


def Success(request):
    ''' When user successfully verify there email '''
    return render(request, 'authenticate/success.html')
