"""
Consilium Speaker's List System
Copyright (C) 2016  Jonas A. Hultén

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# login.views.py
# login-app view bindings
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    # Test if the user is authenticated
    if request.user.is_authenticated:
        # Redirect to main site
        return redirect('/list')
    else:
        # Serve login page
        return render(request, 'login/index.html', {
            'version' : settings.VERSION,
            'authfail' : False,
        })

def auth(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except (KeyError):
        # Be very upset and just throw the fool back
        return index(request)
    else:
        # Attempt authentication
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/login')
        else:
            # Login failed
            return render(request, 'login/index.html', {
                'version' : settings.VERSION,
                'authfail' : True,
            })

def logoff(request):
    logout(request)
    return redirect('/')
