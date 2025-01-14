from pythonosc import dispatcher, osc_server
from ..effects.test_effect_delay import set_delay_time,set_delay_feedback
import glob
class effect_setup():
    def __init__(self):
        self.effects_list = []
    def get_effects_list(self):
        self.effects_list = glob.glob("../effects/*")
    def effect_preset(self):
        dispatcher = dispatcher.Dispatcher()
        #for effectname,effectargs in zip(""):
        dispatcher.map("/delay/time", set_delay_time)
        dispatcher.map("/delay/feedback", set_delay_feedback)
        #dispatcher.map("/reverb/amount", set_reverb_amount)