"""
Consilium Speaker's List System
Copyright (C) 2017 Jonas A. Hultén

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
# userimport.forms.py
# user import app form validators
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserImportForm(forms.Form):
    data = forms.CharField(label='Datablock', required=True,
                           widget=forms.Textarea)

    """Special parse-function, to verify the input data.

    Returns an object containing a user list (users) and error list
    (errors). If an error occured during parsing, errors will be nonempty and
    ulist will be empty. This is to allow returning all parse errors at once,
    rather than a fail-fast method.

    """
    def parse_and_verify(self, verified_data):
        """Internal function for adding errors"""
        def new_error(block, line, message):
            block['errors'].append({
                'line' : line,
                'message' : message,
                })
        datablock = {
            'users' : [],
            'errors' : [],
        }
        ulist = []
        passed = verified_data['data'].split('\r\n')
        lnum = 0
        for line in passed:
            lnum += 1
            cutline = line.split(';')
            if len(cutline) < 6:
                new_error(datablock, lnum, 'Insufficient number of fields')
                continue
            uname = cutline[0].strip()
            fname = cutline[1].strip()
            lname = cutline[2].strip()
            email = cutline[3].strip()
            pwd  = cutline[4].strip()
            code = cutline[5].lower().strip()
            if uname == '' or fname == '' or lname == '' or pwd == '':
                new_error(datablock, lnum, 'Obligatory field missing')
                continue
            if not email == '':
                try: 
                    validate_email(email)
                except ValidationError:
                    new_error(datablock, lnum, 'Malformed email')
                    continue
            if len(pwd) < 8:
                new_error(datablock, lnum, 'Password too short')
                continue
            if not code == 'p':
                code = 'r'
            ulist.append({
                'username' : uname,
                'first-name' : fname,
                'last-name' : lname,
                'email' : email,
                'password' : pwd,
                'code' : code,
            })
        if len(datablock['errors']) == 0:
            datablock['users'] = ulist
        return datablock
