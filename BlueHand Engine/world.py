from actor import Actor
class World:
    def __init__(self):
        self.objects = []

    def tick(self):
        for obj in self.objects:
            obj.tick()

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)
            
    def add_actor(self, obj: Actor) -> None:
        self.objects.append(obj)
    