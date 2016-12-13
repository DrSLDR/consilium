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
# speaker.views.py
# speaker-app view bindings
from django.shortcuts import render, redirect
from .models import Queue, Speaker

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('/')

    # Authenticated user. Load queue data
    first = Queue.objects.filter(queue_id__exact=1)
    second = Queue.objects.filter(queue_id__exact=2)
    return render(request, 'speaker/index.html', {
        'udata' : request.user,
        'first' : first,
        'second' : second,
    })
