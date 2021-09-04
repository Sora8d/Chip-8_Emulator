import sdl2, sdl2.ext
import sys
WHITE = sdl2.ext.Color(255, 255, 255)
BLACK= sdl2.ext.Color(0,0,0)

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)

class Pointer():
    def __init__(self, world, factory, posx=0, posy=0):
        self.position= posx, posy
        self.factory= factory
        self.entity= PointerEntity(world, self.factory.from_color(BLACK, size=(3,3)), *self.position)
        self.color= 0

    def change_pixel_color(self):
        if self.color == 1:
            self.entity.sprite=self.factory.from_color(BLACK, size=(3,3))
            self.entity.sprite.position= self.position
            self.color= 0
        else:
            self.entity.sprite=self.factory.from_color(WHITE, size=(3,3))
            self.entity.sprite.position= self.position
            self.color= 1

class PointerEntity(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx, posy):
        self.sprite= sprite
        self.sprite.position= posx, posy

class sdl2_manager():
    def __init__(self):
        sdl2.ext.init()
        self.window= sdl2.ext.Window("Emulator", size=(192, 96))
        self.window.show()

        self.factory= sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

        self.world=sdl2.ext.World()
        spriterenderer=SoftwareRenderer(self.window)
        self.world.add_system(spriterenderer)

        self.entities= []
        for height in range(32):
            line= []
            for width in range(64):
                line.append(Pointer(self.world, self.factory, width*3, height*3))
            self.entities.append(line)


    def act(self):
        events= sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                sys.exit()
                return 0
        self.world.process()
        return 1

    def clear_screen(self):
        for line in self.entities:
            for entity in line:
                entity.entity.sprite= self.factory.from_color(BLACK, size=(1,1))
                entity.color= 0