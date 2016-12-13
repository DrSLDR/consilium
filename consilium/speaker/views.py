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
from .models import Queue, Speaker, Meeting, Item

# Create your views here.
def index(request):
    # Initial authentication test
    if (not request.user.is_authenticated or not
        request.user.groups.filter(name__in=['Representative',
                                             'Presidium']).exists()):
        return redirect('/')

    # Authenticated user. Prepare data block
    first = Queue.objects.filter(queue_id__exact=1)
    first = first.order_by('timestamp')
    second = Queue.objects.filter(queue_id__exact=2)
    second = second.order_by('timestamp')
    current_meeting = Meeting.objects.get(end_time=None)
    current_item = Item.objects.filter(meeting__exact=current_meeting).last()
    datablock = {
        'udata' : request.user,
        'first' : first,
        'second' : second,
        'm_id': current_meeting.id,
        'i_id': current_item.id,
    }

    # Determine which group the user belongs to and pass accordingly
    if request.user.groups.filter(name='Presidium').exists():
        return render(request, 'speaker/index_pres.html', datablock)
    elif request.user.groups.filter(name='Representative').exists():
        return render(request, 'speaker/index_rep.html', datablock)
