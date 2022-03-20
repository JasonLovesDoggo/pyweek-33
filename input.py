class Movement:
    def __init__(self):
        self.func = []

    def add(self, code, func):
        self.func.append({'code': code, 'func': func})
    
    def run(self, keys):
        for func in self.func:
            if keys[func['code']]:
                func['func']()