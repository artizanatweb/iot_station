from Alarms import Alarms


class AlarmsSingleton:
    __instance = None

    def __init__(self):
        if not AlarmsSingleton.__instance:
            pass
        else:
            self.getInstance()

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Alarms()
        return cls.__instance
