from time import sleep
from pyfldm.appmonitor import AppMonitor
from pyfldm.client import Client
from .base_test_case import BaseTestCase
from utilities.user_prompt import UserPrompt
import base64

class TestClientMain(BaseTestCase):
    def __init__(self) -> None:
        super().__init__()
        self.user_prompt = UserPrompt()
        self.app = AppMonitor()
        self.client = Client()
    
    def setup(self) -> None:
        if self.app.is_running():
            self.app.stop(force_if_unsuccessful=True)
        self.app.start()
    
    def cleanup(self) -> None:
        if self.app.is_running():
            self.app.stop(force_if_unsuccessful=True)
    
    def restart(self) -> None:
        self.app.stop()
        sleep(2)
        self.app.start()

    
    def test_main_tune_and_abort(self):
        self.user_prompt.verify_yes("Set your computer sound volume low, between 10-25% and ensure there is no radio connected to the computer")
        self.client.main.tune()
        assert self.user_prompt.verify_yes("Select Y if you can hear a tone")
        self.client.main.abort()
        assert self.user_prompt.verify_yes("Select Y if the tone turned off")

    def test_main_get_set_toggle_afc(self):
        self.client.main.set_afc(True)
        sleep(1)
        assert self.client.main.get_afc()

        old_state = self.client.main.set_afc(False)
        sleep(1)
        assert old_state
        assert not self.client.main.get_afc()

        new_state = self.client.main.toggle_afc()
        sleep(1)
        assert new_state
        assert self.client.main.get_afc()

    def test_main_get_char_rates(self):
        # TODO: not sure how else to test this
        rates = self.client.main.get_char_rates()
        assert type(rates) == str

    def test_main_get_char_timing(self):
        # TODO: not sure how else to test this
        char1 = "A"
        enc_char1 = char1.encode()
        base16_char1 = base64.b16encode(enc_char1)
        response = self.client.main.get_char_timing(base16_char1)
        assert type(response) == str

    def test_main_get_set_inc_frequency(self):
        pass
    
    def test_main_get_set_toggle_lock(self):
        pass

    def test_main_get_max_macro_id(self):
        pass

    def test_main_get_set_toggle_rsid(self):
        pass

    def test_main_get_set_toggle_txid(self):
        pass

    def test_main_get_set_toggle_squelch(self):
        pass

    def test_main_get_set_squelch_level(self):
        pass

    def test_main_get_status1(self):
        pass

    def test_main_get_status2(self):
        pass

    def test_main_get_trx_state(self):
        pass

    def test_main_get_trx_status(self):
        pass

    def test_main_get_trx_timing(self):
        pass

    def test_main_get_set_wf_sideband(self):
        pass

    def test_main_run_macro(self):
        pass

    def test_main_rx_tx(self):
        # rx
        # rx only
        # rx_tx
        # get_trx_state
        # tx
        pass

    def test_main_set_toggle_reverse(self):
        pass

    def test_main_tune(self):
        pass

    



        