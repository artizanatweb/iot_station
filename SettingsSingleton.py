from Settings import Settings


class SettingsSingleton:
    __instance = None

    def __init__(self):
        if not SettingsSingleton.__instance:
            pass
        else:
            self.getInstance()

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Settings()
        return cls.__instance
