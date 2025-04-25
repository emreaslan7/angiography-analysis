class StateManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(StateManager, cls).__new__(cls)
            cls._instance._data = {}
        return cls._instance

    def set(self, key, value):
        self._data[key] = value

    def get(self, key):
        return self._data.get(key)

