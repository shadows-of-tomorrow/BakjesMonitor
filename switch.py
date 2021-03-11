import tinytuya

CONFIG = {
    "ID": "00042500c82b96020833",
    "IP": "192.168.8.110",
    "KEY": "c7bbe65e472792c9"
}


class Switch:

    def __init__(self):
        self.tuya = tinytuya.OutletDevice(CONFIG["ID"], CONFIG["IP"], CONFIG["KEY"])
        self.tuya.set_version(3.3)
        self.tuya.set_dpsUsed({"1": None})

    def turn_on(self):
        self.tuya.set_status(True)

    def turn_off(self):
        self.tuya.set_status(False)

    def flip(self):
        switch_state = self._get_switch_state()
        self.tuya.set_status(not switch_state)

    def _get_switch_state(self):
        return self.tuya.status()['dps']['1']
