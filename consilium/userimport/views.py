"""
Consilium Speaker's List System
Copyright (C) 2017 Jonas A. Hultén

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
# userimport.views.py
# user import app view bindings
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group

from .forms import UserImportForm

# Create your views here.
@staff_member_required
def index(request):
    # Base variables
    err_data = []
    confirm = ''

    # Check if this was a submission
    if request.method == 'POST':
        # Spawn form instance and backfill
        form  = UserImportForm(request.POST)
        # Test validity
        if form.is_valid():
            # Parse the datablock
            data = form.parse_and_verify(form.cleaned_data)
            err_data = data['errors']
            if len(err_data) == 0:
                # No errors. Continue
                userlist = data['users']
                # Load in group references
                pres = Group.objects.get(name='Presidium')
                rep = Group.objects.get(name='Representative')
                for user in userlist:
                    try:
                        usermodel = User.objects.get(username=user['username'])
                    except User.DoesNotExist:
                        usermodel = User(username=user['username'])
                    usermodel.first_name = user['first-name']
                    usermodel.last_name = user['last-name']
                    usermodel.email = user['email']
                    usermodel.set_password(user['password'])
                    usermodel.save()
                    if user['code'] == 'p':
                        usermodel.groups.set([pres])
                    else:
                        usermodel.groups.set([rep])
                    usermodel.save()
                confirm = len(userlist)

    # GET-request; no data incoming
    else:
        form = UserImportForm()

    return render(request, 'userimport/index.html', {
        'has_permission' : True,
        'site_url' : True,
        'title' : 'User import',
        'form' : form,
        'errors' : err_data,
        'goodnews' : confirm,
    })


