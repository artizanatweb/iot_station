

class Alarms:

    def __init__(self):
        self.__keys = [0]
        self.__alarms = {"not_used": 0}

    def __register(self, type, pin_number):
        # create index
        key = len(self.__keys)
        # add index
        self.__keys.append(key)

        alarm_name = type + "_" + pin_number

        # add alarm
        self.__alarms[alarm_name] = key

        return key

    def get_index(self, type, pin_number):
        alarm_name = type + "_" + pin_number
        index = 0
        try:
            index = self.__alarms[alarm_name]
        except:
            index = self.__register(type, pin_number)

        return index
