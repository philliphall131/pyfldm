YES_OPTIONS = ['Y', 'y']
NO_OPTIONS = ['N', 'n']
YES_NO_OPTIONS = YES_OPTIONS + NO_OPTIONS
class UserPrompt:
    def _get_yes_or_no(self, message):
        response = input(f'\n{message}. (Y/N): ')
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
        
