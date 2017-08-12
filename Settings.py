import ujson as json
import sys


class Settings:
    def __init__(self):
        self.file = "/settings.json"
        self.config = ""

    def load(self):
        try:
            with open(self.file) as f:
                self.config = json.loads(f.read())
        except (OSError, ValueError):
            print("Can't load settings.json file")
            sys.exit(1)

    def get(self, name):
        try:
            self.config[name]
        except:
            return False

        return self.config[name]

    def getRelaySettings(self, name):
        try:
            self.config['relays'][name]
        except:
            return False

        return self.config['relays'][name]
