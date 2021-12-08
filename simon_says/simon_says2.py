from fltk import *
import random
class Gamewin(Fl_Window):
    flashcount = 0
    count = 0
    level = 1
    order = []
    buttons = []
    clicked = []
    flag = 0
    butflag = 0

    def __init__(self,winl,winh):
        Fl_Window.__init__(self, 0, 0, winl, winh,'Simon Says!')
        self.begin()

        self.browsepack = Fl_Group(0,0,self.w(),25)
        self.browsepack.begin()
        self.scoreboard = Fl_Output(0,0,self.w(),25)
        self.scoreboard.value('Current Score: 0')
        self.browsepack.end()
        self.browsepack.type(FL_VERTICAL)

        self.butgroup = Fl_Group(0, 0, self.w(), self.h())
        self.butgroup.begin()

        self.greenbut = Fl_Button(winl//9, (winh-25)//9, winl//3, winh//3)
        self.greenbut.color(FL_GREEN)
        self.greenbut.callback(self.but_cb,0)
        self.greenbut.shortcut('i')
        Gamewin.buttons.append(self.greenbut)

        self.redbut = Fl_Button(winl//9 * 5, (winh-25)//9, winl//3, winh//3)
        self.redbut.color(FL_RED)
        self.redbut.callback(self.but_cb,1)
        self.redbut.shortcut('o')
        Gamewin.buttons.append(self.redbut)

        self.yellowbut = Fl_Button(winl//9, (winh-25)//9 * 5, winl//3, winh//3)
        self.yellowbut.color(FL_YELLOW)
        self.yellowbut.callback(self.but_cb,2)
        self.yellowbut.shortcut('k')
        Gamewin.buttons.append(self.yellowbut)

        self.bluebut = Fl_Button(winl//9 * 5, (winh-25)//9 * 5, winl//3, winh//3)
        self.bluebut.color(FL_BLUE)
        self.bluebut.callback(self.but_cb,3)
        self.bluebut.shortcut('l')
        Gamewin.buttons.append(self.bluebut)

        self.butgroup.end()

        self.startbut = Fl_Button(winl//9 * 4, (winh-25)//9 * 4, winl//9, (winh-25)//9, '&Start')
        self.startbut.callback(self.start_cb)
        self.startbut.take_focus()

        self.end()

        self.resizable(self.butgroup)

    def start_cb(self,wid):
        self.flag = 1
        Gamewin.count = 0
        Gamewin.order = []
        Gamewin.clicked = []
        Gamewin.flashcount = 0
        Gamewin.level = 1
        self.scoreboard.value('Current Score: 0')
        self.rand_cb()

    def but_cb(self,wid,button):
        if self.butflag:
            print('pressed')
            #clicked = []
            if button != Gamewin.order[Gamewin.count]:
                fl_message('Game over')
                self.flag = 0
                return
            else:
                Gamewin.clicked.append(button)
                Gamewin.count += 1
            print(Gamewin.clicked)
            if Gamewin.clicked == Gamewin.order:
                print('passed')
                self.butflag = 0
                Gamewin.level += 1
                Fl.add_timeout(0.4, self.rand_cb)
                self.scoreboard.value(f'Current score: {Gamewin.level - 1}')

    def rand_cb(self):
        if self.flag:
            if len(Gamewin.order) != Gamewin.level:
                choice = random.randrange(0,4)
                Gamewin.order.append(choice)
            if Gamewin.flashcount == Gamewin.level:
                Gamewin.clicked = []
                Gamewin.flashcount = 0
                Gamewin.count = 0
                self.butflag = 1
                return
            print(Gamewin.flashcount)
            print(Gamewin.order)
            print(Gamewin.clicked)
            print(Gamewin.level)


            Fl.add_timeout(0.4, self.interval_to, [Gamewin.buttons[Gamewin.order[Gamewin.flashcount]],Gamewin.buttons[Gamewin.order[Gamewin.flashcount]].color()])

    def interval_to(self,butcolor):
        self.decolor_to(butcolor)
        Gamewin.flashcount += 1
        if Gamewin.flashcount <= Gamewin.level:
            Fl.add_timeout(0.4, self.rand_cb)
        print(Gamewin.flashcount)
        print(Gamewin.order)
        print(Gamewin.clicked)
        print(Gamewin.level)

    def decolor_to(self,butcolor):
        butcolor[0].color(FL_WHITE)
        butcolor[0].redraw()
        Fl.add_timeout(0.25, self.recolor_to, butcolor)

    def recolor_to(self,butcolor):
        butcolor[0].color(butcolor[1])
        butcolor[0].redraw()


app = Gamewin(500,500)
app.show()
Fl.scheme("plastic")
Fl.run()
