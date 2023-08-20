from time import sleep
from pyfldm.appmonitor import AppMonitor
from pyfldm.client import Client
from .base_test_case import BaseTestCase
from utilities.user_prompt import UserPrompt

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
    
    def get_set_toggle(self, set_func:str, get_func:str, tog_func:str) -> bool:
        state1 = set_func(True)
        if not (type(state1) == bool):
            return False, "state1 not of type bool"
        sleep(1)

        state2 = get_func()
        if not (type(state2) == bool):
            return False, "state2 not of type bool"
        if not state2:
            return False, "state2 should be True, was False"

        state3 = set_func(False)
        if not state3:
            return False, "state3 should be True, was False"
        sleep(1)

        state4 = get_func()
        if state4:
            return False, "state4 should be False, was True"

        state5 = tog_func()
        if not state5:
            return False, "state5 should be True, was False"
        sleep(1)

        state6 = get_func()
        if not state6:
            return False, "state6 should be True, was False"
        return True, ""
    
    def test_main_tune_and_abort(self):
        self.user_prompt.verify_yes("Set your computer sound volume low, between 10-25% and ensure there is no radio connected to the computer")
        self.client.main.tune()
        assert self.user_prompt.verify_yes("Select Y if you can hear a tone")
        self.client.main.abort()
        assert self.user_prompt.verify_yes("Select Y if the tone turned off")

    def test_main_get_set_toggle_afc(self):
        get_afc = self.client.main.get_afc
        set_afc = self.client.main.set_afc
        tog_afc = self.client.main.toggle_afc
        result, msg = self.get_set_toggle(set_afc, get_afc, tog_afc)
        assert result, msg

    def test_main_get_char_rates(self):
        # TODO: not sure how else to test this
        rates = self.client.main.get_char_rates()
        assert type(rates) == str

    def test_main_get_char_timing(self):
        # TODO: not sure how else to test this
        test_chars = "ABC"
        response = self.client.main.get_char_timing(test_chars)
        assert type(response) == str

    def test_main_get_set_inc_frequency(self):
        freq1 = self.client.main.get_frequency()
        assert type(freq1) == float

        new_freq = 1405000
        freq2 = self.client.main.set_frequency(new_freq)
        assert type(freq1) == float
        assert freq2 == freq1
        sleep(1)

        freq3 = self.client.main.get_frequency()
        assert freq3 == new_freq
        sleep(1)

        freq4 = self.client.main.inc_frequency(5000)
        assert type(freq1) == float
        assert freq4 == (freq3 + 5000)
        sleep(1)

        freq5 = self.client.main.get_frequency()
        assert freq5 == freq4
        sleep(1)

        freq6 = self.client.main.inc_frequency(-10000)
        assert freq6 == (freq5 - 10000)
        sleep(1)

        freq7 = self.client.main.get_frequency()
        assert freq7 == freq6

    def test_main_get_set_toggle_lock(self):
        get_lock = self.client.main.get_lock
        set_lock = self.client.main.set_lock
        tog_lock = self.client.main.toggle_lock
        result, msg = self.get_set_toggle(set_lock, get_lock, tog_lock)
        assert result, msg

    def test_main_get_max_macro_id(self):
        num = self.client.main.get_max_macro_id()
        assert type(num) == int

    def test_main_get_set_toggle_rsid(self):
        get_rsid = self.client.main.get_rsid
        set_rsid = self.client.main.set_rsid
        tog_rsid = self.client.main.toggle_rsid
        result, msg = self.get_set_toggle(set_rsid, get_rsid, tog_rsid)
        assert result, msg

    def test_main_get_set_toggle_txid(self):
        get_txid = self.client.main.get_txid
        set_txid = self.client.main.set_txid
        tog_txid = self.client.main.toggle_txid
        result, msg = self.get_set_toggle(set_txid, get_txid, tog_txid)
        assert result, msg

    def test_main_get_set_toggle_squelch(self):
        get_squelch = self.client.main.get_squelch
        set_squelch = self.client.main.set_squelch
        tog_squelch = self.client.main.toggle_squelch
        result, msg = self.get_set_toggle(set_squelch, get_squelch, tog_squelch)
        assert result, msg

    def test_main_get_set_squelch_level(self):
        squelch1 = self.client.main.set_squelch_level(55)
        assert type(squelch1) == float
        sleep(1)

        squelch2 = self.client.main.get_squelch_level()
        assert type(squelch2) == float
        assert squelch2 == 55

        squelch3 = self.client.main.set_squelch_level(30)
        assert squelch3 == 55
        sleep(1)

        squelch4 = self.client.main.get_squelch_level()
        assert squelch4 == 30
    
    def test_main_get_set_toggle_reverse(self):
        get_reverse = self.client.main.get_reverse
        set_reverse = self.client.main.set_reverse
        tog_reverse = self.client.main.toggle_reverse
        result, msg = self.get_set_toggle(set_reverse, get_reverse, tog_reverse)
        assert result, msg
        
    def test_main_get_status1(self):
        result = self.client.main.get_status1()
        assert type(result) == str

    def test_main_get_status2(self):
        result = self.client.main.get_status2()
        assert type(result) == str

    def test_main_get_trx_timing(self):
        result = self.client.main.get_tx_timing("Hello World")
        assert type(result) == str

    def test_main_get_set_wf_sideband(self):
        pass

    def test_main_run_macro(self):
        self.user_prompt.verify_yes("Set your computer sound volume low, between 10-25% and ensure there is no radio connected to the computer")
        self.client.main.run_macro(8)
        assert self.user_prompt.verify_yes("Select Y if you can hear a tone")
        self.client.main.abort()
        sleep(2)

    def test_main_rx_tx(self):
        # self.user_prompt.verify_yes("Set your computer sound volume low, between 10-25% and ensure there is no radio connected to the computer")

        # state1 = self.client.main.get_trx_state()
        # assert state1 == "RX"
        # state2 = self.client.main.get_trx_status()
        # assert state2 == "rx"

        # self.client.main.tx()
        # sleep(1)
        # state3 = self.client.main.get_trx_state()
        # assert state1 == "TX"
        # state4 = self.client.main.get_trx_status()
        # assert state2 == "tx"

        # self.client.main.rx()
        # sleep(1)
        # state1 = self.client.main.get_trx_state()
        # assert state1 == "RX"
        # state2 = self.client.main.get_trx_status()
        # assert state2 == "rx"


        # # rx only
        # # rx_tx
        pass

    



        