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
# urls.py
# Consilium project core url bindings
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^(?:login/)?', include('login.urls')),
    url(r'^list/', include('speaker.urls')),
    url(r'^userimport/', include('userimport.urls')),
    url(r'^admin/', admin.site.urls),
]
