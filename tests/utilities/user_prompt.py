YES_OPTIONS = ['Y', 'y']
NO_OPTIONS = ['N', 'n']
SKIP_OPTIONS = ['S', 's']
YES_NO_OPTIONS = YES_OPTIONS + NO_OPTIONS
YES_NO_SKIP_OPTIONS = YES_NO_OPTIONS + SKIP_OPTIONS
class UserPrompt:
    def _get_yes_or_no(self, message):
        response = input(f'\n{message} (Y/N): ')
        while response not in YES_NO_OPTIONS:
            response = input(f'Invalid selection. Try again\n{message}. (Y/N): ')
        return response
    
    def _get_yes_or_skip(self, message):
        response = input(f'\n{message} (Y/N)(S to skip test): ')
        while response not in SKIP_OPTIONS:
            response = input(f'Invalid selection. Try again\n{message}. (Y/N/S): ')
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
    
    def skip_option(self, what_to_check):
        response = self._get_yes_or_skip(what_to_check)
        if response in SKIP_OPTIONS:
            return 'skip'
        elif response in YES_OPTIONS:
            return True
        return False
        
