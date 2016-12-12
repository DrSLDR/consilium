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

@channel_session_user_from_http
def ws_add(message):
    if not message.user.is_authenticated:
        return
    Group('master').add(message.reply_channel)
    uname = message.user.first_name + " " + message.user.last_name
    meeting = Meeting.objects.first()
    try:
        speaker = Speaker.objects.get(user=message.user, meeting=meeting)
    except Speaker.DoesNotExist:
        speaker = Speaker(user=message.user, name=uname, meeting=meeting)
        speaker.save()

@channel_session_user
def ws_message(message):
    if not message.user.is_authenticated:
        return
    if message.content['text'] == 'speak':
        _request_to_speak(message)
    elif message.content['text'] == 'strike':
        _request_to_be_struck(message)

def _request_to_speak(message):
    uname = message.user.first_name + " " + message.user.last_name
    item = Item.objects.first()
    meeting = item.meeting
    speaker = Speaker.objects.get(user=message.user, meeting=meeting)
    q = listlogic.add_to_queue(speaker, item)
    if q == 0:
        return
    _send_to_master({
        'speaker' : uname,
        'queue' : q,
        'method' : 'add',
    })
    
def _request_to_be_struck(message):
    uname = message.user.first_name + " " + message.user.last_name
    item = Item.objects.first()
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

def _send_to_master(data):
    Group('master').send({'text': json.dumps(data)})
