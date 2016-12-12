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
# speaker.listlogic.py
# Speaker-app list logic backend
from .models import Speaker, Queue, Log, Item

def which_queue(speaker, item):
    n = Queue.objects.filter(speaker__exact=speaker)
    n = n.filter(item__exact=item).count()
    if n > 0:
        return 0
    n = Log.objects.filter(speaker__exact=speaker)
    n = n.filter(item__exact=item).count()
    if n > 0:
        return 2
    else:
        return 1

def add_to_queue(speaker, item):
    n = which_queue(speaker, item)
    if n > 0:
        q = Queue(speaker=speaker, item=item, queue_id=n)
        q.save()
    return n

def spoken(speaker, item):
    q = Queue.objects.get(speaker=speaker, item=item)
    l = Log(speaker=speaker, item=item, timestamp=q.timestamp)
    l.save()
    q.delete()

def strike(speaker, item):
    try:
        q = Queue.objects.get(speaker=speaker, item=item)
    except Queue.DoesNotExist:
        return 0
    n = q.queue_id
    q.delete()
    return n
