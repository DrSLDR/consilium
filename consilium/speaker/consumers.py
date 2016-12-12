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
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http, channel_session_user
from .models import Speaker, Meeting

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

@channel_session
def ws_echo(message):
    if 'username' not in message.channel_session:
        return
    Group('chat').send({
        'text': json.dumps({
            'message': message.content['text'],
            'username': message.channel_session['username']
        }),
    })
