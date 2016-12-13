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
# speaker.admin.py
# speaker-app admin bindings. Allows reading of log and speaker lists from admin interface.
from django.contrib import admin
from .models import Speaker, Log, Meeting, Item, Queue

# Register your models here.
admin.site.register(Speaker)
admin.site.register(Log)
admin.site.register(Meeting)
admin.site.register(Item)
admin.site.register(Queue)
