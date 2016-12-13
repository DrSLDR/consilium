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
# speaker.consumers.py
# Speaker-app WebSocket data consumer
import json
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http, channel_session_user
from .models import Speaker, Meeting, Item
from . import listlogic
from django.utils import timezone

@channel_session_user_from_http
def ws_add(message):
    if not message.user.is_authenticated:
        return
    Group('master').add(message.reply_channel)

@channel_session_user
def ws_message(message):
    if not message.user.is_authenticated:
        return

    # Parse content
    data = _parse_message(message.content['text'])

    # Determine action
    command = data['command']
    if command  == 'speak':
        _request_to_speak(message, data)
    elif command == 'strike':
        _request_to_be_struck(message, data)
    elif command == 'next':
        _order_next(message, data)
    elif command == 'new-item':
        _order_new_item(message, data)
    elif command == 'new':
        _manual_add(message, data)
    elif command == 'kill':
        _order_struck(message, data)
    elif command == 'end-meeting':
        _order_end(message, data)
    elif command == 'open':
        _order_open(message, data)
    else:
        _send_to_master({
            'oops': 'command not understood',
            'original': message.content,
        })

def _request_to_speak(message, data):
    uname = message.user.first_name + " " + message.user.last_name
    item = Item.objects.get(id=data['iid'])
    meeting = item.meeting
    uname = message.user.first_name + " " + message.user.last_name
    try:
        speaker = Speaker.objects.get(user=message.user, meeting=meeting)
    except Speaker.DoesNotExist:
        _register_speaker(name=uname, meeting=meeting, user=message.user)
    speaker = Speaker.objects.get(user=message.user, meeting=meeting)
    q = listlogic.add_to_queue(speaker, item)
    if q == 0:
        return
    _send_to_master({
        'speaker' : uname,
        'queue' : q,
        'method' : 'add',
    })
    
def _request_to_be_struck(message,data):
    uname = message.user.first_name + " " + message.user.last_name
    item = Item.objects.get(id=data['iid'])
    meeting = item.meeting
    speaker = Speaker.objects.get(user=message.user, meeting=meeting)
    q = listlogic.strike(speaker, item)
    if q == 0:
        return
    _send_to_master({
        'speaker': uname,
        'queue': q,
        'method': 'strike',
    })

def _order_next(message, data):
    item = Item.objects.get(id=data['iid'])
    q = listlogic.get_next_speaker(item)
    if q == 0:
        return
    speaker = q.speaker
    uname = speaker.name
    n = q.queue_id
    listlogic.spoken(speaker, item)
    _send_to_master({
        'speaker': uname,
        'queue': n,
        'method': 'strike',
    })

def _order_new_item(message, data):
    citem = Item.objects.get(id=data['iid'])
    meeting = citem.meeting
    nitem = Item(name=data['args'], meeting=meeting)
    nitem.save()
    _send_to_master({
        'speaker' : 'Chronos',
        'queue' : 0,
        'method' : 'end',
    })

def _manual_add(message, data):
    name = data['args']
    item = Item.objects.get(id=data['iid'])
    meeting = item.meeting
    try:
        speaker = Speaker.objects.get(name=name, meeting=meeting)
    except Speaker.DoesNotExist:
        speaker = _register_speaker(name, meeting)
    q = listlogic.add_to_queue(speaker, item)
    if q == 0:
        return
    _send_to_master({
        'speaker' : name,
        'queue' : q,
        'method' : 'add',
    })

def _order_struck(message, data):
    name = data['args']
    item = Item.objects.get(id=data['iid'])
    meeting = item.meeting
    speaker = Speaker.objects.get(name=name, meeting=meeting)
    q = listlogic.strike(speaker, item)
    if q == 0:
        return
    _send_to_master({
        'speaker' : name,
        'queue' : q,
        'method' : 'strike',
    })

def _order_end(message, data):
    item = Item.objects.get(id=data['iid'])
    meeting = item.meeting
    meeting.end_time = timezone.now()
    meeting.save()
    _send_to_master({
        'speaker' : 'Thanatos',
        'queue': 0,
        'method': 'end',
    })

def _order_open(message, data):
    mname = data['args']
    meeting = Meeting(name=mname)
    meeting.save()
    item = Item(name='Start', meeting=meeting)
    item.save()
    _send_to_master({
        'speaker' : 'Gaia',
        'queue' : 0,
        'method' : 'end',
    })

def _parse_message(text):
    splits = text.split(':')
    return {
        'command' : splits[0],
        'args' : splits[1],
        'iid' : splits[2],
    }

def _register_speaker(name, meeting, user=None):
    speaker = Speaker(user=user, name=name, meeting=meeting)
    speaker.save()
    return speaker

def _send_to_master(data):
    Group('master').send({'text': json.dumps(data)})
