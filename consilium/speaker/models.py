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
# speaker.models.py
# speaker-app models. Here's where all the fun stuff happens.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Meeting(models.Model):
    name = models.CharField('meeting name', max_length=200)
    start_time = models.DateTimeField('starting time')
    end_time = models.DateTimeField('ending time', null=True, blank=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField('item name', max_length=200)
    meeting = models.ForeignKey(Meeting)

    def __str__(self):
        return self.meeting.__str__() + ": " + self.name

class Speaker(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField('name', max_length=100)
    meeting = models.ForeignKey(Meeting)
    count = models.IntegerField('times spoken', default=0)

    def __str__(self):
        return self.meeting.__str__() + ": " + self.name

class Queue(models.Model):
    speaker = models.ForeignKey('speaker', Speaker)
    item = models.ForeignKey(Item)
    timestamp = models.DateTimeField('timestamp', default=timezone.now)
    queue_id = models.IntegerField('queue id', default=1)

    def __str__(self):
        return self.speaker.__str__()

class Log(models.Model):
    speaker = models.ForeignKey('speaker', Speaker)
    item = models.ForeignKey(Item)
    timestamp = models.DateTimeField('timestamp', default=timezone.now)

    def __str__(self):
        return self.speaker.__str__()
