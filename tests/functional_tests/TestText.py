from pyfldm.AppMonitor import AppMonitor
from .BaseTestCase import BaseTestCase
from utilities.UserPrompt import UserPrompt

class TestText(BaseTestCase):
    user_prompt = UserPrompt()

    def test_app_start(self):
        app = AppMonitor()

    def test_apple(self):
        assert self.user_prompt.verify_yes("Choose yes")

    def test_two(self):
        assert True