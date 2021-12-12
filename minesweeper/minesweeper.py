from fltk import *
import random

class Minesweep(Fl_Window):
    pictures = ['0.png','1.png','2.png','3.png','4.png','5.png','6.png','7.png','8.png','mine.png','flag.png']
    altered = ['0a.png','1a.png','2a.png','3a.png','4a.png','5a.png','6a.png','7a.png','8a.png','minea.png','flaga.png']
    square = Fl_PNG_Image('square.png')
    minecount = 10 #mines set and time elapsed
    minecount_1 = minecount #just for reference
    sidelength = 10
    def __init__(self, w, h):
        '''instantiates the class and creates the game'''
        super().__init__(0, 0, w, h, 'Minesweeper')

        #variables used to keep track:
        self.revealed = [] #revealed squares
        self.time = 0
        self.buttons = [] #buttons
        self.mines = [] #buttons that are mines
        self.to_start = False #game started
        self.to_reveal = []

        self.group = Fl_Group(0,0,w,h)
        self.group.begin()

        self.outp = Fl_Output(0, 0, w, 50) #outputs score

        self.size = w//Minesweep.sidelength

        for buty in range(Minesweep.sidelength):
            for butx in range(Minesweep.sidelength):
                but = Fl_Button(butx * self.size, 50 + buty*((h-50)//Minesweep.sidelength), self.size, self.size)
                self.buttons.append([but,None,False,None,None])
                self.buttons[-1][0].callback(self.but_cb, buty*Minesweep.sidelength + butx)
                self.buttons[-1][0].image(Minesweep.square.copy(self.size, self.size))
                self.buttons[-1][4] = Minesweep.square
                self.buttons[-1][0].redraw() #creates length x length grid with an image and adds callbacks

        self.group.end()

        self.mineset()
        self.num_assign()
        self.resizable(self.group)

        with open('minescores.txt','r') as file:
            self.highscore = file.read().strip().split(',') #gets the current high score from file

    def time_to(self):
        '''adds 1 to the time every second elapsed'''
        self.time += 1
        self.outp.value(f'Time: {self.time}') #adjusts output value
        Fl.repeat_timeout(1.0,self.time_to) #repeats the adding every 1 second

    def mineset(self):
        '''sets the mines in the grid'''
        if Minesweep.minecount == 0: #if there are already enough mines function ends
            return
        randbut = random.randrange(0,Minesweep.sidelength**2)
        if self.buttons[randbut][1] == None: #if the chosen square is not already a mine
            self.buttons[randbut][1] = 9 #set it as a mine
            self.mines.append(randbut)
            Minesweep.minecount -= 1 #adds one to minecount
        self.mineset()

    def num_assign(self):
        '''assigns the numbers for the squares of the grid'''
        for but in range(len(self.buttons)):
            if self.buttons[but][1] != 9: #if the button iterated through grid is not a mine
                self.buttons[but][1] = self.detect(but) #pass button through function

    def detect(self,but):
        '''detects the number of mines around square'''
        bombs = 0
        for num in range(-1,2):
            for num1 in range(-1,2):
                if but % Minesweep.sidelength + num1 in range(0,Minesweep.sidelength): #squares beyond right and left side column counted
                    if but//Minesweep.sidelength + num in range(0,Minesweep.sidelength): #squares beyong top and bottom row not counted
                        if self.buttons[but + (Minesweep.sidelength*num) + num1][1] == 9:
                            bombs += 1 #if there is a bomb, add 1
        return bombs

    def reveal(self,but):
        '''finds the amount of squares to reveal'''
        for num in range(-1,2):
            for num1 in range(-1,2):
                if but + (num*Minesweep.sidelength) + num1 in range(0,Minesweep.sidelength**2) and but%Minesweep.sidelength + num1 in range(0,Minesweep.sidelength) and but//Minesweep.sidelength + num in range(0,Minesweep.sidelength):
                    #like the previous function, only detects relevant squares
                    if self.buttons[but][1] == 0: #if the button has no mines around it (number 0)
                        if self.buttons[but + (num*Minesweep.sidelength) + num1][1] in range(0,9): #if the squares around the square is a non-zero number
                            if but + (num*Minesweep.sidelength) + num1 not in self.to_reveal: #if said square is not already revealed
                                self.to_reveal.append(but + (num*Minesweep.sidelength) + num1) #add it to the "to add" list
                    if self.buttons[but + (num*Minesweep.sidelength) + num1][1] == 0: #if a square containing 0 is detected around
                        if but + (num*Minesweep.sidelength) + num1 not in self.revealed: #if that square is not already added
                            self.revealed.append(but + (num*Minesweep.sidelength) + num1)
                            self.reveal(but + (num*Minesweep.sidelength) + num1) #pass the square through the same function
                    else:
                        if but not in self.to_reveal: #if the button pressed is not already revealed
                            self.to_reveal.append(but) #just show the button if there are no "0"s around

    def but_cb(self,wid,value):
        '''reveals the buttons to the user and detects when game ends'''
        if not self.to_start: #if the press is the first press of the game
            Fl.add_timeout(1.0,self.time_to) #starts the timeout
            self.to_start = True #prevents future starts of the timeout
        if Fl.event_button() == FL_RIGHT_MOUSE:
            if not self.buttons[value][2] and not self.buttons[value][3]: #if the button is not flagged and is not revealed already
                wid.image(Fl_PNG_Image(Minesweep.pictures[10]).copy(wid.w(),wid.h())) #pastes image of flag
                self.buttons[value][2] = True
                self.buttons[value][3] = True #turns on flags
                self.buttons[value][4] = Fl_PNG_Image(Minesweep.pictures[10]) #sets list index 4 to original image, preserves quality
            elif self.buttons[value][3]: #if box is already flagged
                wid.image(Minesweep.square.copy(wid.w(),wid.h())) #sets image as original square picture
                self.buttons[value][2] = False
                self.buttons[value][3] = False #turns off flags
                self.buttons[value][4] = Minesweep.square
        elif Fl.event_button() == FL_LEFT_MOUSE:
            if not self.buttons[value][2]: #if the button is not already revealed
                self.reveal(value) #pass the function

                for but in self.to_reveal:
                    pic = Fl_PNG_Image(Minesweep.pictures[self.buttons[but][1]]) #original, high quality picture
                    self.buttons[but][0].image(pic.copy(self.buttons[but][0].w(),self.buttons[but][0].h()))
                    self.buttons[but][0].redraw() #applies image to buttons and redraws
                    self.buttons[but][2] = True #True for revealed
                    self.buttons[but][4] = pic #adds original picture to index 4 for high quality redrawing
                    if but not in self.revealed:
                        self.revealed.append(but)
                    if self.buttons[but][1] == 9: #if mine is clicked, game ends as a loss (False)
                        self.game_end(False)
                self.to_reveal = []

                if len(self.revealed) == (Minesweep.sidelength**2) - Minesweep.minecount_1: #if all non-mine squares are clicked/revealed, game ends as a win (True)
                    self.game_end(True)


    def game_end(self,case):
        '''reveals images and overwrites files depending on win or loss'''
        Fl.remove_timeout(self.time_to) #removes the timer
        if case:
            if self.time >= int(self.highscore[1]): #if game is won and time is higher than current high score
                fl_message(f'You win! Your time is {self.time} seconds. The current score is {self.highscore[1]} held by {self.highscore[0]}')
            else: #when game is won and a time lower than the high score is achieved
                name = fl_input(f'You win! You got a score of {self.time} seconds, beating {self.highscore[0]}\'s score of {self.highscore[1]} seconds. Enter name: ')
                with open('minescores.txt','w') as file:
                    if name == None: #if nothing is inputted as a name
                        file.write('Anonymous' + ',' + str(self.time))
                    else:
                        file.write(name + ',' + str(self.time))
            pic = Fl_PNG_Image('mineb.png') #undetonated mine picture
            for mine in self.mines: #for every mine
                self.buttons[mine][0].image(pic.copy(self.buttons[mine][0].w(),self.buttons[mine][0].h()))
                self.buttons[mine][0].redraw() #applies picture and redraws
                self.buttons[mine][2] = True #mine is revealed
                self.buttons[mine][3] = False #mine cannot be flagged
                self.buttons[mine][4] = pic
        else: #game is lost
            fl_message(f'You lose... Time: {self.time} seconds')
            for but in self.buttons:
                if not but[2] or (but[3] and but[1] == 9): #if the button has not yet been revealed and if a bomb is flagged
                    pic = Fl_PNG_Image(Minesweep.altered[but[1]])
                    but[0].image(pic.copy(but[0].w(),but[0].h()))
                    but[0].redraw() #applies relevant original photo and redraws
                    but[2] = True #revealed flag
                    but[3] = False #square cannot be flagged
                    but[4] = pic
                elif but[3] and but[1] != 9: #if square if flagged but is not a mine
                    pic = Fl_PNG_Image('minec.png') #crossed out mine picture
                    but[0].image(pic.copy(but[0].w(),but[0].h()))
                    but[0].redraw()
                    but[2] = True #square is revealed
                    but[3] = False #square cannot be flagged
                    but[4] = pic

    def draw(self):
        '''overriding draw to resize pictures upon resizing buttons'''
        super().draw()
        for but in self.buttons:
            but[0].image(but[4].copy(but[0].w(),but[0].h()))
            but[0].redraw() #redraws the button with its original picture

length = 600
game = Minesweep(length, length + 50)
game.show()
Fl.run()
