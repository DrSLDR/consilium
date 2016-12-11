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

# consumers.py
# WebSocket data consumer

import json
import urllib.parse as ulp
from channels import Group
from channels.sessions import channel_session

@channel_session
def ws_add(message):
    query = ulp.parse_qs(message['query_string'])
    if 'username' not in query:
        return
    Group('chat').add(message.reply_channel)
    message.channel_session['username'] = query['username'][0]

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
