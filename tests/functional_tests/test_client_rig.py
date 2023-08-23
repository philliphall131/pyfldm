from time import sleep
from pyfldm.appmonitor import AppMonitor
from pyfldm.client import Client
from .base_test_case import BaseTestCase
from utilities.user_prompt import UserPrompt

class TestClientRig(BaseTestCase):
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
    
    def test_rig_get_set_bandwidth(self):
        result1 = self.client.rig.set_bandwidths(['100', '150'])
        result2 = self.client.rig.get_bandwidths()
        result3 = self.client.rig.get_bandwidth()
        result4 = self.client.rig.set_bandwidth("150")
    
    def test_rig_get_set_modes(self):
        result1 = self.client.rig.set_modes(['CW', 'SSB'])
        result2 = self.client.rig.get_modes()
        result3 = self.client.rig.get_mode()
        result4 = self.client.rig.set_mode("CW")
    
    def test_rig_get_set_name(self):
        result1 = self.client.rig.set_name("Test Rig 1")
        result2 = self.client.rig.get_name()
    
    def test_rig_set_frequency(self):
        result1 = self.client.rig.set_frequency(1500)
    
    def test_rig_get_notch(self):
        result1 = self.client.rig.get_notch()
    
    def test_rig_set_pwrmeter(self):
        result1 = self.client.rig.set_pwrmeter(50)

    def test_rig_set_smeter(self):
        result1 = self.client.rig.set_smeter(50)
    
    #TODO: uncomment and update once endpoints functional
    # def test_rig_control(self):
    #     self.client.rig.take_control()
    #     sleep(2)
    #     self.client.rig.release_control()
    #     sleep(2)