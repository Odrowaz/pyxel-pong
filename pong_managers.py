import pyxel

class BaseManager():
    def __init__(self):
        self.list = []
        pass
    
    def register(self, *args):
        self.list.extend(args)
        
    def tick(self):
        pass

class UpdateManager(BaseManager):
    def tick(self):
        for updatable in self.list:
            updatable.update()
            
class DrawManager(BaseManager):
    def tick(self):
        pyxel.cls(0)
        for drawable in self.list:
            drawable.draw()
            
class PhysicsManager(BaseManager):
    def tick(self):
        for i, collidable1 in enumerate(self.list):
            for j in range(i + 1, len(self.list)):
                collidable2 = self.list[j]
                
                x_colliding = (collidable1.x < collidable2.x + collidable2.width and 
                            collidable1.x + collidable1.width > collidable2.x - collidable2.width)
                y_colliding = (collidable1.y < collidable2.y + collidable2.height and 
                            collidable1.y + collidable1.height > collidable2.y - collidable2.height)
                
                if x_colliding and y_colliding:
                    self.collide(collidable1, collidable2)
                    
    def collide(self, collidable1, collidable2):
        collidable1.collide(collidable2)
        collidable2.collide(collidable1)
