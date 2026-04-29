class Actor:
    def __init__(self, name: str):
        self.name = name
        self._abilities = {}
        self._memory = {}

    def can(self, ability):
        self._abilities[type(ability)] = ability
        return self

    def ability_to(self, ability_type):
        return self._abilities[ability_type]

    def remember(self, key: str, value):
        self._memory[key] = value

    def recall(self, key: str, default=None):
        return self._memory.get(key, default)

    def attempts_to(self, *tasks):
        for task in tasks:
            task.perform_as(self)
