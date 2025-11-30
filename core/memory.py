class Memory:
    def __init__(self):
        self.history = []

    def add(self, item):
        self.history.append(item)

    def get(self):
        return self.history
