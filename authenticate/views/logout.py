from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import View


class SignOutView(LoginRequiredMixin, View):
    ''' Logoutview will log out the current login user '''

    def get(self, request):
        logout(request)
        return redirect('landing')


def logout_func(request):
    logout(request)
    request.user.session_set.all().delete()
    del request.session['currency']
    return HttpResponseRedirect('/')
