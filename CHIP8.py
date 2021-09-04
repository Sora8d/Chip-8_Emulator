import time
from CHIP_SDL2 import sdl2_manager
def run():
    #SetGraphics
    #SetInput
    manager= sdl2_manager()
    Chip= Chip8(manager)


    doc= open("./roms/IBMLogo.ch8", "rb")
    Chip.initialize()
    Chip.load_Game(doc)
    while True:
        Chip.emulateCycle()
        manager.act()
    pass

class Chip8():
    def __init__(self, sdl_manager) -> None:
        self.sdl_manager= sdl_manager
        self.memory= [None for x in range(4096)]
        #So these are all supossedly 2 bytes long, that supposedly a short from C is able to store inside itself.
        self.opcode= 0
        self.I= 0
        self.pc= 0

        self.pixels= self.sdl_manager.entities

        #Setting flag
        self.V={}
        for position in range(16):
            self.V[position]= None

        #Timers
        self.delay_timer= None
        self.sound_timer= None

        #Stack and stack pointer
        self.stack= []
        self.sp= 0
        self.instructions= {0x0000: self.instructs_for_zero, 0x1000: self.instructs_for_one, 0xA000: self.instructs_for_a, 0x2000: self.instructs_for_two, 0x6000: self.instructs_for_six, 0x7000: self.instructs_for_seven, 0xD000: self.instructs_for_d}

    def initialize(self):
        self.pc= 0x200
        self.opcode=0
        self.I=0
        self.sp=0        

        #Clear display
        
        #Clear stack
        #Clear registers V0-VF
        #Clear memory

        #Load fontset
        fontset=[0xF0, 0x90, 0x90, 0x90, 0xF0,0x20, 0x60, 0x20, 0x20, 0x70,0xF0, 0x10, 0xF0, 0x80, 0xF0,0xF0, 0x10, 0xF0, 0x10, 0xF0,0x90, 0x90, 0xF0, 0x10, 0x10,0xF0, 0x80, 0xF0, 0x10, 0xF0,0xF0, 0x80, 0xF0, 0x90, 0xF0,0xF0, 0x10, 0x20, 0x40, 0x40,0xF0, 0x90, 0xF0, 0x90, 0xF0,0xF0, 0x90, 0xF0, 0x10, 0xF0,0xF0, 0x90, 0xF0, 0x90, 0x90,0xE0, 0x90, 0xE0, 0x90, 0xE0,0xF0, 0x80, 0x80, 0x80, 0xF0,0xE0, 0x90, 0x90, 0x90, 0xE0,0xF0, 0x80, 0xF0, 0x80, 0xF0,0xF0, 0x80, 0xF0, 0x80, 0x80]
        for index, font in enumerate(fontset):
            self.memory[index] = font

        #reset timers
        return

    def load_Game(self, file):
        buffer = file.read()
        for index, byte in enumerate(buffer):
            self.memory[512+index]= byte


    def emulateCycle(self):
        self.drawFlag= 0
        #Fech Opcode
        self.opcode= (self.memory[self.pc] << 8) | self.memory[self.pc+1]
        #Decode Opcode
        _dec_opcode= self.opcode & 0xF000
        self.pc += 2
        #Execute Opcode
        try:
            self.instructions[_dec_opcode](self.opcode)
        except KeyError as e:
            raise KeyError(hex(self.opcode))
        #Update timers, not implemented yet
        time.sleep(0.017)
        return

    def instructs_for_zero(self, opcode):
        #Clear screen
        _further_opcode= opcode & 0x000F
        if _further_opcode == 0x0000:
            self.sdl_manager.clear_screen()

    def instructs_for_one(self,opcode):
        position= opcode & 0x0FFF
        self.pc= position

    def instructs_for_two(self, opcode):
        #Jump to NNN in pc
        position= opcode & 0x0FFF
        self.stack.append(self.pc)
        self.sp += 1
        self.pc= position

    def instructs_for_six(self,opcode):
        pos_v= (opcode & 0x0F00) >> 8
        value= opcode & 0x00FF
        self.V[pos_v] = value

    def instructs_for_seven(self,opcode):
        pos_v= (opcode & 0x0F00) >> 8
        value= opcode & 0x00FF
        self.V[pos_v] += value

    def instructs_for_a(self, opcode):
        #Register I
        position= opcode&0x0FFF
        self.I = position

    def instructs_for_d(self,opcode):
        x= self.V[(opcode & 0x0F00) >> 8]
        y= self.V[(opcode & 0x00F0) >> 4]
        height= opcode& 0x000F
        sprites= self.memory[self.I: self.I+height]
        self.V[0xF]= 0
        pr= 0
        spriteBits= [format(sp, "b") for sp in sprites]
        
        for y_index, byte in enumerate(spriteBits):
            if byte != "0":
                filltobyte= 8-len(byte)
                byte= "0"*filltobyte + byte
            for x_index, bit in enumerate(byte):
                if int(bit) == 1:
                    pixel_pos= self.pixels[y+y_index][x+x_index]
                    if pixel_pos == 1:
                        self.V[0xF]
                    pixel_pos.change_pixel_color()
        self.drawFlag= 1
        return

run()