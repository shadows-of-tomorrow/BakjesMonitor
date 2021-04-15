import os
import json
import tinytuya


class Switch:

    def __init__(self, switch_id):
        self.switch_id = switch_id
        self.tuya = self._read_tuya_config()
        self.tuya.set_version(3.3)
        self.tuya.set_dpsUsed({"1": None})

    def _read_tuya_config(self):
        root_dir = os.path.dirname(__file__)
        config_dir = os.path.join(root_dir, 'config')
        with open(config_dir+'/tuya.txt') as f:
            config = json.loads(f.read())[self.switch_id]
        return tinytuya.OutletDevice(config['ID'], config['IP'], config['KEY'])

    def turn_on(self):
        self.tuya.set_status(True)

    def turn_off(self):
        self.tuya.set_status(False)

    def flip(self):
        switch_state = self._get_switch_state()
        self.tuya.set_status(not switch_state)

    def _get_switch_state(self):
        return self.tuya.status()['dps']['1']
