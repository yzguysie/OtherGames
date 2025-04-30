class Actor:
    def __init__(self):
        raise NotImplementedError

    def tick(self):
        raise NotImplementedError
    
    def draw(self, surface):
        raise NotImplementedError