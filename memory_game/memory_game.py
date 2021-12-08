from fltk import *
import random
from PIL import Image
import io

def img_resize(fname,width): #function to resize images
    '''resizes any image type using high quality PIL library'''
    img = Image.open(fname) #opens all image formats supported by PIL
    w,h = img.size
    height = int(width*h/w)  #correct aspect ratio
    img = img.resize((width, height), Image.BICUBIC) #high quality resizing
    mem = io.BytesIO()  #byte stream memory object
    img.save(mem, format="PNG") #converts image type to PNG byte stream
    siz = mem.tell() #gets size of image in bytes without reading again
    return Fl_PNG_Image(None, mem.getbuffer(), siz)

def randomizer(pictures):
    '''list of integers are scrambled to used as indexes to determine image order'''
    rand_pics = []
    rand_ints = [0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11]
    random.shuffle(rand_ints) #shuffles list of indexes
    #assigns integers as indexes for list of pictures
    for integer in rand_ints:
        rand_pics.append(pictures[2:][integer]) #adds image of the random index
    return rand_pics

def img_reveal(wid,detail):
    '''determines what is to be revealed, hidden when button is clicked'''
    global buts #variables are` global to avoid convoluted lists
    global pics_matched
    global flag
    global clicks
    added_img = detail[0][detail[1]]
    if flag == 0:
        detail[4].extend([added_img,detail[1],None]) #tracks img name & buttons pressed
        wid.image(img_resize(added_img,120))
        flag = 1
        clicks += 1
    elif flag == 1:
        detail[4][2] = detail[1]
        if detail[1] != detail[4][1]: #prevents first button from counting if pressed
            wid.image(img_resize(added_img,120))
            if added_img == detail[4][0]: #for if images match
                buts[detail[4][1]].image().inactive()
                buts[detail[1]].image().inactive()
                buts[detail[4][1]].deactivate() #deactivates/inactivates matching wids/pics
                buts[detail[1]].deactivate()
                flag = 0
                detail[4].clear() #resets tracker
                pics_matched += 1
                if pics_matched == 12: #if all pics are matched
                    win_screen = fl_input(f'You win! Enter name ({clicks} clicks): ')
                    record_writer(score_sorter(win_screen,clicks)) #applies score to leaderboard
            else:
                flag = 2 #for if images don't match
            clicks += 1
    else:
        if detail[1] not in (detail[4][1], detail[4][2]) and detail[4][1] != detail[4][2]:
            buts[detail[4][1]].image(detail[2])
            buts[detail[4][2]].image(detail[2])
            buts[detail[4][1]].redraw() #reverts button back to original pic and
            buts[detail[4][2]].redraw() #redraws button for change to show
            wid.image(img_resize(added_img,120))
            detail[4][:3] = [added_img,detail[1],None]
            flag = 1
            clicks += 1 #clicks are in each statement so pressing same button
                        #does not increase click count

def score_sorter(name,clicks):
    '''sorts and stores scores of all playthroughs in separate file records.txt'''
    with open('records.txt','r') as score:
        records = score.read().strip().split(',') #formats score for proper reading
    for data in records: #name is in format ['name:score']
        if clicks < int(data[data.find(':')+1:]): #number of clicks as integer
            records.insert(records.index(data),str(name)+':'+str(clicks)) #inserts score in proper ranking
            break #inserts score and breaks to prevent multiple insertions
    with open('records.txt','w') as score:
        score.write(','.join(records)) #converts back to score's original format
    return records

def record_writer(records):
    '''changes the leaderboards (highscores.txt) according to sorted scores'''
    with open('highscores.txt','w') as file:
        file.write('LEADERBOARDS:') #rewrites leaderboard to prevent repeats of leaderboard
    with open('highscores.txt','a+') as file: #appends to rewritten leaderboard
        for score_name in records:
            if score_name[score_name.find(':')+1:] not in '999999999': #does not add default score (prevents out of index error)
                file.write('\n'+ str(score_name[:score_name.find(':')]) + ' - ' + str(score_name[score_name.find(':')+1:]) + ' clicks')

Pokemon = ['pokemon.png', 'pokemonbackground.png', 'alakazam.png', 'beedrill.png', 'mr-mime.png', 'gengar.png', 'ditto.png', 'pikachu.png', 'gyarados.png', 'snorlax.png', 'dragonite.png', 'exeggutor.png', 'kangaskhan.png', 'charmander.png']
pic_order = randomizer(Pokemon)

win = Fl_Window(0,0,1200,800,'Memory Game!')
win.begin()

back_pic = Fl_PNG_Image(Pokemon[0])
back_pic = back_pic.copy(190,190) #image for 'unchosen' images
background = Fl_PNG_Image(Pokemon[1])
background = background.copy(1200,800)

scenery = Fl_Box(0,0,1200,800) #serves as background scenery
scenery.image(background)

#variables used for counting:
clicks = 0 #counts score in clicks
pics_matched = 0 #keeps track of tracked images
flag = 0 #flags circumstances during button click
track = [] #keeps track of images and indexes

buts = []
spec_button = 0
for row in range(4):
    for col in range(6):
        buts.append(Fl_Button(col*200,row*200,200,200))
        buts[-1].clear_visible_focus()
        buts[-1].image(back_pic) #applies cosmetic changes to most recent button
        buts[-1].box(FL_NO_BOX)
        buts[-1].callback(img_reveal,[pic_order, spec_button, back_pic, clicks, track])
        spec_button += 1
        #uses loops to create button array
        #spec_button used as index to determine button to put picture on

win.end()
win.show()
Fl.run()
