############################################################################
# 
#  File: user_prompt.py
#  Copyright(c) 2023, Phillip Hall. All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#  USA
#
############################################################################

YES_OPTIONS = ['Y', 'y']
NO_OPTIONS = ['N', 'n']
YES_NO_OPTIONS = YES_OPTIONS + NO_OPTIONS
class UserPrompt:
    def _get_yes_or_no(self, message):
        response = input(f'\n{message} (Y/N): ')
        while response not in YES_NO_OPTIONS:
            response = input(f'Invalid selection. Try again\n{message}. (Y/N): ')
        return response

    def verify_yes(self, what_to_check):
        response = self._get_yes_or_no(what_to_check)
        if response in YES_OPTIONS:
            return True
        return False
    
    def verify_no(self, what_to_check):
        response = self._get_yes_or_no(what_to_check)
        if response in NO_OPTIONS:
            return True
        return False
        
