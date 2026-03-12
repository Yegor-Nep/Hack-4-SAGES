class Facade:
    data = {}
    def __init__(self):
        self.data = {} 

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

facade_singleton = Facade()

