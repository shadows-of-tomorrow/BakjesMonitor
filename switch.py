import tinytuya

class Switch:
    
    def __init__(self):
        self.config = {"ip": "192.168.8.110", "id": "00042500c82b96020833", "key": "c7bbe65e472792c9"}
        self.tuya = tinytuya.OutletDevice(self.config["id"], self.config["ip"], self.config["key"])
        self.tuya.set_version(3.3)
        self.tuya.set_dpsUsed({"1": None})
        
    def _get_state(self):
        return self.tuya.status()
        
if __name__ == "__main__":
    switch = Switch()
    print(switch._get_state())