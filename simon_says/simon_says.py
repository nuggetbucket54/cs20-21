from fltk import *
import random
class Gamewin(Fl_Window):
    flashcount = 0
    count = 0
    order = []
    buttons = []
    clicked = []
    flag = 0
    butflag = 0

    def __init__(self,winl,winh):
        Fl_Window.__init__(self, 0, 0, winl, winh,'Simon Says!')
        self.begin()

        self.butgroup = Fl_Group(0, 0, self.w(), self.h())
        self.butgroup.begin()

        self.greenbut = Fl_Button(winl//9, winh//9, winl//3, winh//3)
        self.greenbut.color(fl_rgb_color(124,255,91))
        self.greenbut.callback(self.but_cb,0)
        Gamewin.buttons.append(self.greenbut)

        self.redbut = Fl_Button(winl//9 * 5, winh//9, winl//3, winh//3)
        self.redbut.color(fl_rgb_color(255,55,55))
        self.redbut.callback(self.but_cb,1)
        Gamewin.buttons.append(self.redbut)

        self.yellowbut = Fl_Button(winl//9, winh//9 * 5, winl//3, winh//3)
        self.yellowbut.color(FL_YELLOW)
        self.yellowbut.callback(self.but_cb,2)
        Gamewin.buttons.append(self.yellowbut)

        self.bluebut = Fl_Button(winl//9 * 5, winh//9 * 5, winl//3, winh//3)
        self.bluebut.color(fl_rgb_color(81,169,255))
        self.bluebut.callback(self.but_cb,3)
        Gamewin.buttons.append(self.bluebut)

        self.butgroup.end()

        self.startgroup = Fl_Group(winl//9 * 4, winh//9 * 4, winl//9, winh//9)
        self.startgroup.begin()
        self.startbut = Fl_Button(winl//9 * 4, winh//9 * 4, self.startgroup.w(), self.startgroup.h())
        self.startbut.callback(self.start_cb)
        self.startgroup.end()

        self.end()

        self.resizable(self.butgroup)

    def start_cb(self,wid):
        self.flag = 1
        Gamewin.count = 0
        Gamewin.order = []
        Gamewin.clicked = []
        self.rand_cb()

    def but_cb(self,wid,button):
        if self.butflag:
            #clicked = []
            if button != Gamewin.order[Gamewin.count]:
                print(button)
                print(Gamewin.order)
                print(Gamewin.count)
                print(Gamewin.order[Gamewin.count])
                fl_message('Game over')
                self.flag = 0
                return
            else:
                Gamewin.clicked.append(button)
                Gamewin.count += 1
            if Gamewin.clicked == Gamewin.order:
                Fl.add_timeout(1.0, self.rand_cb)
                self.butflag = 0
            print(Gamewin.clicked)
            '''
            while True:
                clicked.append(info[0])
                #for num in range(Gamewin.count):
                    #print(num)
                print(info[0])
                print(Gamewin.order)
                print(Gamewin.order[current])
                if info[0] != Gamewin.order[current]:
                    print('bad')
                    Gamewin.order = []
                    break
                if clicked == Gamewin.order:
                    break
                current += 1
            '''

    def rand_cb(self):
        if self.flag:
            choice = random.randrange(0,4)
            Gamewin.order.append(choice)
            print(Gamewin.order)
            print(Gamewin.flashcount)
            Gamewin.clicked = []
            for but in range(len(Gamewin.order)):
                Fl.add_timeout(1.0, self.decolor_to, [Gamewin.buttons[Gamewin.order[but]],Gamewin.buttons[Gamewin.order[but]].color()])
                '''if but:
                    Fl.add_timeout(1.0, self.decolor_to, [Gamewin.buttons[Gamewin.order[but]],Gamewin.buttons[Gamewin.order[but]].color()])
                else:
                    self.decolor_to([Gamewin.buttons[Gamewin.order[but]],Gamewin.buttons[Gamewin.order[but]].color()])'''
                Gamewin.flashcount += 1
            Gamewin.count = 0
            Gamewin.flashcount = 0
            self.butflag = 1


    def decolor_to(self,butcolor):
        butcolor[0].color(FL_WHITE)
        butcolor[0].redraw()
        Fl.add_timeout(0.25, self.recolor_to, butcolor)

    def recolor_to(self,butcolor):
        butcolor[0].color(butcolor[1])
        butcolor[0].redraw()

    def interval_to(self):
        pass

app = Gamewin(500,500)
app.show()
Fl.run()
