import sys
from pyfldm.appmonitor import AppMonitor
from pyfldm.client import Client
from .base_test_case import BaseTestCase
from utilities.user_prompt import UserPrompt

class TestClientFldigi(BaseTestCase):
    def __init__(self) -> None:
        super().__init__()
        self.user_prompt = UserPrompt()
        self.app = AppMonitor()
        self.client = Client()
    
    def setup(self) -> None:
        if self.app.is_running():
            self.app.stop(force_if_unsuccessful=True)
        self.app.start()
        self.client.modem.set_by_name("CW")
    
    def cleanup(self) -> None:
        if self.app.is_running():
            self.app.stop(force_if_unsuccessful=True)
    
    def test_fldigi_name(self):
        name = self.client.fldigi.name()
        assert name == 'fldigi'
    
    def test_fldigi_name_and_version(self):
        name_version = self.client.fldigi.name_and_version()
        name_version_list = name_version.split(" ")
        name = name_version_list[0]
        version = name_version_list[1]
        assert name == 'fldigi'
        version_list = version.split(".")
        assert len(version_list) == 3
    
    def test_fldigi_list(self):
        method_list = self.client.fldigi.list()
        assert type(method_list) == list
    
    def test_fldigi_version(self):
        version = self.client.fldigi.version()
        version_list = version.split(".")
        assert len(version_list) == 3
    
    def test_fldigi_version_struct(self):
        version = self.client.fldigi.version_struct()
        assert type(version) == dict
    
    def test_fldigi_config_dir(self):
        config_dir = self.client.fldigi.config_dir()
        assert type(config_dir) == str
        if sys.platform != "win32":
            fl_dir = config_dir.split("/")[-2]
            assert fl_dir == ".fldigi"
        else:
            #TODO
            pass
    
    # ##** fldigi.terminate tested in test_appmonitor::test_app_graceful_shutdown **##
    
    