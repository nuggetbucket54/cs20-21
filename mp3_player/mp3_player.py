from fltk import *
import os
import subprocess as sp
import signal
from mutagen.mp3 import MP3
import random

def win_cb(wid):
    '''terminates playing songs during the closing of the app'''
    global playing
    if playing != 0: #if there is a song playing when the app closes
        playing.send_signal(signal.SIGTERM)
    wid.hide() #actually closes the app

def dir_cb(wid,playlist):
    '''adds mp3 files from a directory to a dictionary for playing'''
    global songlist
    dir = fl_dir_chooser('Choose a directory: ','')
    if dir == None:
        return #prevents error if no directory is chosen
    for song in os.listdir(dir): #gets all the song names
        if song[-4:] == '.mp3': #makes sure they are mp3
            playlist[song[:-4]] = os.path.normpath(os.path.join(dir,song)) #creates the key (song name) with a value (file path)
    browse.clear() #resets browser (for if new directory is added)
    for rep in sorted(playlist.keys(), key = lambda x: x.lower()):
        browse.add(rep) #sorts dict alphabetically
    browse.select(1)
    browse.take_focus() #sets focus to playlist

def clear_cb(wid,songlist):
    '''clears all data used previously given'''
    global playing
    songlist.clear()
    browse.clear() #resets the entire app by clearing all data
    outp.value('')
    Fl.remove_timeout(songtime_cb) #stops timeouts from continuing
    if playing != 0:
        playing.send_signal(signal.SIGTERM) #stops song if one is playing

def shuf_cb(wid):
    '''sets/resets a flag for the player to detect if shuffle mode is on'''
    global shuffle
    if wid.color() == fl_rgb_color(255,212,253):
        wid.color(fl_rgb_color(217,166,255)) #adds a darker color to signal the activation of shuffle
        shuffle = 1 #sets shuffle to True or 1 as a flag
    else:
        wid.color(fl_rgb_color(255,212,253))
        shuffle = 0 #resets shuffle back to 0

def choose_cb(wid,flag):
    '''selects the song to play'''
    global chosen
    global songlist
    global playing
    global shuffle
    if browse.size() == 0:
        return #prevents error if browser is empty
    if flag[0]: #if button is play, previous, skip
        if not flag[1]: #ensure that play button (with flag False/0) will always play selected song
            chosen = browse.value()
        elif not shuffle: #if shuffle is off (False/0)
            if chosen + flag[1] > browse.size(): #if skip is pressed at end of playlist
                browse.select(1)
                chosen = 1 #loops back to the first song of the playlist
            elif chosen + flag[1] == 0: #if previous is pressed at beginning of playlist
                browse.select(browse.size()) #selects the last song
                chosen = browse.size()
            else:
                browse.select(chosen + flag[1])
                chosen += flag[1] #otherwise navigates the playlist normally
        elif shuffle:
            randsong = random.randrange(1,len(songlist)+1) #randomly selects a line from the browser
            while chosen - 1 == randsong:
                randsong = random.randrange(1,len(songlist)+1)
            chosen = randsong
            browse.select(chosen) #selects the randomly picked song
        outp.value('Currently playing: ' + sorted(songlist.keys(), key = lambda x:x.lower())[chosen - 1])
        #shows playing song in Fl_Output
        play_cb(sorted(songlist.keys(), key = lambda x:x.lower())[chosen - 1],chosen - 1)
    elif flag[1] == 2: #if remove button was pressed
        remsong = browse.value() #currently selected
        if sorted(songlist.keys(), key = lambda x:x.lower())[chosen - 1] == sorted(songlist.keys(), key = lambda x:x.lower())[remsong - 1]:
            # ^if the song removed is the song playing
            if playing != 0: #if something is already playing
                playing.send_signal(signal.SIGTERM) #stops playing the song
            outp.value('')
        songlist.pop(sorted(songlist.keys(), key = lambda x:x.lower())[remsong - 1]) #removes currently selected song from dict and browser
        browse.remove(remsong)
        browse.select(remsong) #selects the song that had removed song's index
    browse.take_focus() #gives focus back to the browser, enables scrolling after choosing song

def play_cb(chosen,nextsong):
    '''plays the selected song from choose_cb'''
    global playing
    global songlist
    if playing == 0: #if nothing is playing
        playing = sp.Popen(['vlc','--intf','dummy', songlist[chosen]]) #plays the song
    else:
        playing.send_signal(signal.SIGTERM) #stops previously playing to play new song
        playing = sp.Popen(['vlc','--intf','dummy', songlist[chosen]]) #plays the song
    song = MP3(songlist[chosen])
    Fl.remove_timeout(songtime_cb) #removes timeouts left by other songs
    Fl.add_timeout(song.info.length,songtime_cb,nextsong) #reimplements timeout for song length

def songtime_cb(data):
    '''function called after timeout to autoplay'''
    global songlists
    Fl.remove_timeout(songtime_cb) #stops any remaining timeouts
    choose_cb(None,[1,1]) #autoplays by putting the song back into the choose function

def stop_cb(wid,action):
    '''for stopping the playing of songs'''
    global playing
    if browse.size() == 0 or playing == 0: #prevents errors if browser is empty or nothing is playing
        return
    playing.send_signal(action) #stops playing
    playing = 0
    outp.value('') #clears the browser
    browse.take_focus() #gives focus back to browser
    Fl.remove_timeout(songtime_cb)

def go_cb(wid,flag):
    '''for navigating to a specific song'''
    global songlist
    global chosen
    if flag == 0:
        browse.topline(1) #goes to and selects the top
        browse.select(1)
    elif flag == 1:
        browse.bottomline(len(songlist)) #goes to and selects the bottom
        browse.select(len(songlist))
    else:
        browse.topline(chosen) #places the chosen song at the top
        browse.select(chosen)

songlist = {}
chosen = 0
playing = 0
shuffle = 0

win = Fl_Window(0,0,600,500,"epic mp3 player")
win.begin()

vertpack = Fl_Pack(0,0,win.w(),400)
vertpack.begin()

bar = Fl_Menu_Bar(0,0,0,20) #toolbar and some functions
bar.add('&File/&Add a directory', 0, dir_cb, songlist)
bar.add('&Clear', 0, clear_cb, songlist)
bar.add('&Go/&Top', 0, go_cb, 0)
bar.add('&Go/&Bottom', 0, go_cb, 1)
bar.add('&Go/&Current', 0, go_cb, None)

outp = Fl_Output(0,0,0,30) #output to display what is playing
outp.color(fl_rgb_color(250,255,73))
outp.textcolor(FL_RED)

browse = Fl_Hold_Browser(0,0,0,350) #playlist for songs
browse.take_focus()
browse.color(fl_rgb_color(240,254,255))

vertpack.end()
vertpack.type(FL_VERTICAL)
vertpack.resizable(browse)

horipack = Fl_Pack(0,400,win.w(),100)
horipack.begin()

prevbut = Fl_Button(0,400,100,0,'@#<<') #previous button
prevbut.tooltip('Go to previous song (ALT + Left)')
prevbut.callback(choose_cb,[1,-1])
prevbut.shortcut(FL_ALT|FL_Left)
prevbut.color(fl_rgb_color(255,212,253))

playbut = Fl_Button(100,400,100,0,'@#+2>') #play button
playbut.tooltip('Play song (Enter)')
playbut.callback(choose_cb,[1,0])
playbut.shortcut(FL_Enter)
playbut.color(fl_rgb_color(255,212,253))

nextbut = Fl_Button(200,400,100,0,'@#>>') #skip button
nextbut.tooltip('Skip to next song (ALT + Right)')
nextbut.callback(choose_cb,[1,1])
nextbut.shortcut(FL_ALT|FL_Right)
nextbut.color(fl_rgb_color(255,212,253))

stopbut = Fl_Button(300,400,100,0,'@#-2square') #stop button
stopbut.tooltip('Stop currently playing song (Space)')
stopbut.callback(stop_cb,signal.SIGTERM)
stopbut.shortcut(32)
stopbut.color(fl_rgb_color(255,212,253))

delbut = Fl_Button(400,400,100,0,'@#1+') #remove song button
delbut.tooltip('Remove selected song (x)')
delbut.callback(choose_cb,[False,2])
delbut.shortcut('x')
delbut.color(fl_rgb_color(255,212,253))

shufbut = Fl_Button(500,400,100,0,'@#reload') #shuffle mode button
shufbut.tooltip('Activate shuffle (s)')
shufbut.callback(shuf_cb)
shufbut.shortcut('s')
shufbut.color(fl_rgb_color(255,212,253))

horipack.end()
horipack.type(FL_HORIZONTAL)
horipack.resizable(browse)

win.end()
win.resizable(browse)
win.show()
win.callback(win_cb)

Fl.scheme('gtk+')
Fl.run()
