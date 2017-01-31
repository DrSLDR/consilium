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
    if request.user.is_staff:
        return redirect('/admin')
    if (not request.user.is_authenticated or not
        request.user.groups.filter(name__in=['Representative',
                                             'Presidium']).exists()):
        return redirect('/')

    # Determine if user is in the Presidium
    pres = request.user.groups.filter(name='Presidium').exists()

    # Test if there is an active meeting
    try:
        current_meeting = Meeting.objects.get(end_time=None)
    except Meeting.DoesNotExist:
        # No meeting. Give landing page
        if pres:
            return render(request, 'speaker/no_meeting_pres.html', {})
        else:
            return render(request, 'speaker/no_meeting_rep.html', {})

    # Authenticated user. Prepare data block
    first = Queue.objects.filter(queue_id__exact=1)
    first = first.order_by('timestamp')
    second = Queue.objects.filter(queue_id__exact=2)
    second = second.order_by('timestamp')
    current_item = Item.objects.filter(meeting__exact=current_meeting).last()
    datablock = {
        'udata' : request.user,
        'first' : first,
        'second' : second,
        'item': current_item,
    }

    # Determine which group the user belongs to and pass accordingly
    if pres:
        return render(request, 'speaker/index_pres.html', datablock)
    else:
        return render(request, 'speaker/index_rep.html', datablock)
