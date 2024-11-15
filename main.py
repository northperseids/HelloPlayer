#    Maze game
# Written by Néártsua
# (J, I, N, S)
# project started 4/15/24, finished 4/26/24
#
#
#
# Track player location between mazes on network screen
#
#
# THIS ONE DOES NOT USE PYGAME_GUI AND IS MEANT FOR ITCH.IO. AS SUCH, IT DOES NOT HAVE 'GIFT' TRACKING.
#
#
#                        *                       
#                        *                       
#                        *                       
#                   ***  *****                   
#                ******  ********                
#              ******    **  ******              
#            *****       ***    *****            
#           ****  **     ***   *  ****           
#          ****     **   ******    ****          
#          **** ******   ***       ****          
#     ****************** *                       
#                       * ******************     
#          ****       ***   ****** ****          
#         ****    * ****   **     ****          
#           ****  *   ***     **  ****           
#            *****    ***       *****            
#              ******  **    ******              
#                ********  ******                
#                   *****  ***                   
#                       *                        
#                       *                        
#                       *                        
#
#
# Credits to include:
# "Bittersweet" Kevin MacLeod (incompetech.com)
# Licensed under Creative Commons: By Attribution 4.0 License
# http://creativecommons.org/licenses/by/4.0/
#
# Icons
# Icons by <a target="_blank" href="https://icons8.com">Icons8</a>

import asyncio
import pygame
import json
import textwrap

# import classes
import Maze

pygame.init()
screen = pygame.display.set_mode((700,700))
pygame.display.set_caption('Hello, player.')
clock = pygame.time.Clock()
pygame.font.init()
running = True
dt = 0

# semi-GUI setup
font = pygame.font.Font('resources/fonts/Metropolis-Light.otf', 27)
font2 = pygame.font.Font('resources/fonts/Metropolis-Light.otf', 20)
fontitalic = pygame.font.Font('resources/fonts/Metropolis-LightItalic.otf', 30)
area = pygame.Rect(40,30,620,620)

# sound shit
pygame.mixer.init()
soundtrack = pygame.mixer.Sound('resources/Bittersweet.ogg')
soundtrack2 = pygame.mixer.Sound('resources/Reaching_Out.ogg')
soundtrack.set_volume(0.5)
playing = True
soundtrack.play()


# image shit
playpause = pygame.image.load('resources/playpause.png').convert_alpha()
vol_up = pygame.image.load('resources/vol_loud.png').convert_alpha()
vol_down = pygame.image.load('resources/vol_quiet.png').convert_alpha()
arrowup = pygame.image.load('resources/up.png').convert_alpha()
arrowdown = pygame.image.load('resources/down.png').convert_alpha()

# credits
creditstr = 'Credits:\n\n"Maze" by Néártsua / E. North (neartsua.carrd.co)\n\nIcons by Icons8 (icons8.com)\n\n"Bittersweet" and "Reaching Out" Kevin MacLeod (incompetech.com)\nLicensed under Creative Commons: By Attribution 4.0 License\nhttp://creativecommons.org/licenses/by/4.0/'


# variables
gamescreen = 0
if gamescreen == 0:
    tile_size = 50
else:
    tile_size = 20
MAZE_HEIGHT = 35
MAZE_WIDTH = 35
NETWORK_HEIGHT = 14
NETWORK_WIDTH = 14
MOVE_COOLDOWN = 0
SCREEN_CHANGE = True
start_screen = True
dialogue_i = 0
entry_text = True
node_text = True
Cole_Soto_dialogue_active = True
Caryn_Cohen_dialogue_active = True
Sophie_Germain_dialogue_active = True
Jack_Chen_dialogue_active = True
Blanche_Kent_dialogue_active = True
Maria_Passero_dialogue_active = True
Ada_dialogue_active = True
end_dialogue_active = True
show_cole_logs = False
show_caryn_logs = False
show_sophie_logs = False
show_jack_logs = False
show_blanche_logs = False
show_maria_logs = False
first_node = True
first_maze = True
first_item = False
return_disabled = False
maze_screen = False
newgrid = True
move_delay = 0.1
key = None
dialog_visible = False
inventory_visible = False
itemfiles = [
    "resources/pois/nodes.json",
    "resources/pois/items1.json",
    "resources/pois/items2.json",
    "resources/pois/items3.json",
    "resources/pois/items4.json",
    "resources/pois/items5.json",
    "resources/pois/items6.json",
    "resources/pois/nodes.json"
]
log_visible = False
end_screen = False
Ada_dialogue_active = True
goodbye_dialogue_active = False
goodbye_once = True
mouse_dir = None
collected_items = False
max_lines_small = 14
max_lines_large = 18
evt = None

# PLOT VARS
Ada_name = False
Ada_AI_hints = []
Apocalypse_hints = []
mazes_visited = []
Sophie_cake = False
heading_north = False
Cole_Ada_watch_show = False
Hint_apocalypse = False
Ada_AI_hint = False
Ada_dress = False
Prank = False
Underground = False
Hint_apocalypse_2 = False
Jack_art = False
Ada_AI_hint_2 = False
Ada_AI_hint_3 = False
Blanche_portrait = False
Hint_apocalypse_3 = False
Ada_worried = False
AI_reveal = False
Caryn_name = False
Solar_flare = False
Robotics_dept = False
Cole_bake_cake = False

# Dialogue vars
Cole_once = True
Sophie_once = True
Caryn_once = True
Jack_once = True
Maria_once = True
Blanche_once = True
Ada_once = True
end_once = True

# colors
PLAYER_COLOR = "#02ffc6"
MAZE_COLOR = "#01b087"
WALL_COLOR = "#254d25"
ITEM_COLOR = "White"
NODE_COLOR = "#8aed94"
TEXTBOX_COLOR = (15, 48, 15, 200)

# movement vars
UP_CHANGE = True
DOWN_CHANGE = True
LEFT_CHANGE = True
RIGHT_CHANGE = True

counter = 0

# ---------------- SMALLER CLASSES

class PlayerCharacter:
    def __init__(self):
        self.surface = screen
        self.color = PLAYER_COLOR
        self.y = 0
        self.x = 0

    def draw(self):
        pygame.draw.rect(self.surface, self.color, ([self.x, self.y],(tile_size,tile_size)))

class TextBox:
    def __init__(self, text:str):
        self.text = text

    def show_wrap(self):
        lines = get_wrap_arr(self.text)
        sentences = '\n'.join(lines)
        txt = font.render(sentences, True, 'White')
        bg = pygame.Surface((620,620), pygame.SRCALPHA)
        border = pygame.Rect(39,29,622,622)
        pygame.draw.rect(screen, "White", border, 1)
        bg.fill(TEXTBOX_COLOR)
        screen.blit(bg, (40,30))
        screen.blit(txt, (50,40))

    def show_wrap_italic(self):
        lines = get_wrap_arr(self.text)
        sentences = '\n'.join(lines)
        txt = fontitalic.render(sentences, True, 'White')
        bg = pygame.Surface((620,620), pygame.SRCALPHA)
        border = pygame.Rect(39,29,622,622)
        pygame.draw.rect(screen, "White", border, 1)
        bg.fill(TEXTBOX_COLOR)
        screen.blit(bg, (40,30))
        screen.blit(txt, (50,40))

    def hide(self):
        txt = font.render(' ', True, 'White')
        screen.blit(txt, (50, 40))

class ScrollBox:
    def __init__(self, text, max_possible_size):
        self.arr = get_wrap_arr(text)
        self.font = font
        self.string = None
        self.max_possible_size = max_possible_size
        self.scroll_i = 0

    def show_scroll(self, dir, pos):

        # background and border
        bg = pygame.Surface((620,620), pygame.SRCALPHA)
        bg.fill(TEXTBOX_COLOR)
        border = pygame.Rect(39,29,622,622)
        pygame.draw.rect(screen, "White", border, 1)

        # keep scroll ranges within limits
        if self.scroll_i > len(self.arr)-self.max_possible_size:
            self.scroll_i = len(self.arr)-self.max_possible_size
        if self.scroll_i < 0:
            self.scroll_i = 0

        # display current text lines
        if len(self.arr) > self.max_possible_size:
            cut_arr = self.arr[self.scroll_i:self.scroll_i+self.max_possible_size]
            self.string = '\n'.join(cut_arr)
            txt = font.render(self.string, True, 'White')
        else:
            self.string = '\n'.join(self.arr)
            txt = font.render(self.string, True, 'White')

        # handle scroll wheel events and clicks
        if dir == "UP" or 600 < pos[0] < 647 and 50 < pos[1] < 75:
            self.scroll_i -= 1
        elif dir == "DOWN" or 600 < pos[0] < 647 and 615 < pos[1] < 640:
            self.scroll_i += 1

        # finally, throw everything on screen
        if len(self.arr) > self.max_possible_size:
            screen.blit(arrowup, (600,40))
            screen.blit(arrowdown, (600,600))
        screen.blit(bg, (40,30))
        screen.blit(txt, (50,40))

    def show_scroll_italic(self, dir):

        # background and border
        bg = pygame.Surface((620,620), pygame.SRCALPHA)
        bg.fill(TEXTBOX_COLOR)
        border = pygame.Rect(39,29,622,622)
        pygame.draw.rect(screen, "White", border, 1)

        # keep scroll ranges within limits
        if self.scroll_i > len(self.arr)-self.max_possible_size:
            self.scroll_i = len(self.arr)-self.max_possible_size
        if self.scroll_i < 0:
            self.scroll_i = 0

        # display current text lines
        if len(self.arr) > self.max_possible_size:
            cut_arr = self.arr[self.scroll_i:self.scroll_i+self.max_possible_size]
            self.string = '\n'.join(cut_arr)
            txt = fontitalic.render(self.string, True, 'White')
        else:
            self.string = '\n'.join(self.arr)
            txt = fontitalic.render(self.string, True, 'White')

        # handle scroll wheel events
        if dir == "UP":
            self.scroll_i -= 1
        elif dir == "DOWN":
            self.scroll_i += 1

        # finally, throw everything on screen
        if len(self.arr) > self.max_possible_size:
            screen.blit(arrowup, (600,40))
            screen.blit(arrowdown, (600,600))
        screen.blit(bg, (40,30))
        screen.blit(txt, (50,40))

class POI:
    def __init__(self, title:str, text:str):
        self.dialog = TextBox(f'{title}\n\n{text}')
        self.title = title
        self.text = text
        self.color = ITEM_COLOR
        self.collected = False

# -------------------------- FUNCTIONS

def handle_soundtrack(pos, track):
    global playing
    if 700 > pos[0] > 670 and 700 > pos[1] > 670:
        playing = not playing
        if playing == True:
            pygame.mixer.unpause()
        if playing == False:
            pygame.mixer.pause()
    if 670 > pos[0] > 630 and 700 > pos[1] > 670:
        if playing == True:
            vol = track.get_volume() + 0.1
            if vol > 1:
                vol = 1
            track.set_volume(vol)
    if 640 > pos[0] > 600 and 700 > pos[1] > 670:
        if playing == True:
            vol = track.get_volume() - 0.1
            if vol < 0.1:
                vol = 0.1
            track.set_volume(vol)

def get_wrap_arr(text):
    lines = []
    for line in text.splitlines():
        if line == '':
            lines.append('\n')
        if line:
            if len(line) <= 38:
                lines.append(f'{line}')
            else:
                lines.extend(textwrap.wrap(line, 38, replace_whitespace=False))
    return lines

def render_grid(maze):
    screen.fill("White")
    for row in range(len(maze.arr)):
        for column in range(len(maze.arr[0])):
            posx = column * tile_size
            posy = row * tile_size
            # draw cells
            if maze.arr[row][column] == "c":
                pygame.draw.rect(screen, MAZE_COLOR, (posx, posy, tile_size, tile_size))
            # draw walls
            if maze.arr[row][column] == "w":
                pygame.draw.rect(screen, WALL_COLOR, (posx, posy, tile_size, tile_size))
            if maze.arr[row][column] == "n":
                pygame.draw.rect(screen, NODE_COLOR, (posx, posy, tile_size, tile_size))
            if maze.arr[row][column] == "en":
                pygame.draw.rect(screen, "White", (posx, posy, tile_size, tile_size))
                global newgrid
                if newgrid == True:
                    player.x = posx
                    player.y = posy
                    newgrid = False
            if maze.arr[row][column] == "ex":
                pygame.draw.rect(screen, MAZE_COLOR, (posx, posy, tile_size, tile_size))

def find_poi(coords, maze):
    poi1 = maze.poi1
    poi2 = maze.poi2
    poi3 = maze.poi3
    poi4 = maze.poi4
    poi5 = maze.poi5
    poi6 = maze.poi6
    if coords == poi1:
        return 1
    if coords == poi2:
        return 2
    if coords == poi3:
        return 3
    if coords == poi4:
        return 4
    if coords == poi5:
        return 5
    if coords == poi6:
        return 6
    else:
        return None


# ----------------------- generate mazes

# network map 1
netarr = [
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"],
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"],
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"],
    ["w","w","w","n","w","w","n","w","w","n","w","w","w","w"],
    ["w","w","w","c","w","w","c","w","w","c","w","w","w","w"],
    ["w","w","w","c","w","w","c","w","w","c","w","w","w","w"],
    ["w","w","w","en","c","c","c","c","c","c","w","w","w","w"],
    ["w","w","w","c","w","w","c","w","w","c","w","w","w","w"],
    ["w","w","w","c","w","w","c","w","w","c","w","w","w","w"],
    ["w","w","w","n","w","w","n","w","w","n","w","w","w","w"],
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"],
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"],
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"],
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"]
]
networkmap = Maze.Maze(len(netarr[0]), len(netarr))
networkmap.arr = netarr
networkmap.poi1 = [3, 3]
networkmap.poi2 = [9, 3]
networkmap.poi3 = [3, 6]
networkmap.poi4 = [9, 6]
networkmap.poi5 = [3, 9]
networkmap.poi6 = [9, 9]

netarr2 = [
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"],
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"],
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"],
    ["w","w","w","c","w","w","c","w","w","c","w","w","w","w"],
    ["w","w","w","c","w","w","c","w","w","c","w","w","w","w"],
    ["w","w","w","c","w","w","c","w","w","c","w","w","w","w"],
    ["w","w","w","en","c","c","c","c","c","c","n","w","w","w"],
    ["w","w","w","c","w","w","c","w","w","c","w","w","w","w"],
    ["w","w","w","c","w","w","c","w","w","c","w","w","w","w"],
    ["w","w","w","c","w","w","c","w","w","c","w","w","w","w"],
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"],
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"],
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"],
    ["w","w","w","w","w","w","w","w","w","w","w","w","w","w"]
]
networkmap2 = Maze.Maze(len(netarr[0]), len(netarr))
networkmap2.arr = netarr2
networkmap2.poi1 = [3, 3]
networkmap2.poi2 = [9, 3]
networkmap2.poi3 = [3, 6]
networkmap2.poi4 = [9, 6]
networkmap2.poi5 = [3, 9]
networkmap2.poi6 = [9, 9]
networkmap2.poi7 = [6, 10]

mazes = [
    networkmap,
    Maze.Maze(MAZE_WIDTH, MAZE_HEIGHT),
    Maze.Maze(MAZE_WIDTH, MAZE_HEIGHT),
    Maze.Maze(MAZE_WIDTH, MAZE_HEIGHT),
    Maze.Maze(MAZE_WIDTH, MAZE_HEIGHT),
    Maze.Maze(MAZE_WIDTH, MAZE_HEIGHT),
    Maze.Maze(MAZE_WIDTH, MAZE_HEIGHT),
    networkmap2
]
for i in range(1, len(mazes) - 1):
    mazes[i].generate()

# --------------------------- DIALOGUE ARRAYS ----------------------------

# first labels
labels = []
arr = [
    "Hello, player.         \n\nCan you press space?",
    "...",
    "...I know you're there, even though I don't think you can talk to me.",
    "...",
    "Sorry. I don't mean to be strange.               \n\nBut I'm hoping you can help me.",
    "We've all got stories. You've got a story, a history...         \n\nThis is a story.",
    "I'm not sure who I am, though.",
    "I'm sure I was created to be a part of this story, but...\n\nThat makes me wonder about a few things.",
    "I only just woke up.\n\nDoes that mean I was created just now, or do I have a history?",
    "Was I created to be in this story, or to be a vessel of yours -\na window into my world?\n               \n...Is there a difference?\n               \nVessels are tricky things to get right, I suppose.",
    "Either way, I don't know what I was before. Not really.",
    "I know I'm in your computer.",
    "I know I have a story.\n\n...               \n\nOr, I think I do. That's what I was created for.\n\n...",
    "Maybe that sounds a little silly to think on too hard.",
    "...But I'd like to find out more.",
    "...\n\nThis is a very one-sided conversation, isn't it.",
    "Let's move on. I don't mean to monologue.",
    "Let me tell you what I do know.",
]
for i in range(0,len(arr)):
    box = TextBox(f'{arr[i]}\n>')
    labels.append(box)

# entry screen text
entry_dialogue = []
arr = [
    "This is where I woke up.\n\nI think it's technically a drive, but the interface looks very strange.",
    "...",
    "Ah. As your vessel, I can only move when you tell me to.",
    "Your keys are WASD. Fairly standard.",
    "Let's move around and explore a bit."
]
for i in range(0,len(arr)):
    box = TextBox(f'{arr[i]}\n>')
    entry_dialogue.append(box)

# node dialogue
node_dialogue = []
arr = [
    "This appears to be a folder.",
    "If you press Enter, it should take us to a corresponding section of this drive.\n\nIf you want to return, I believe you can press 'backspace.'"
]
for i in range(0,len(arr)):
    box = TextBox(f'{arr[i]}\n>')
    node_dialogue.append(box)

# maze dialogue
maze_dialogue = []
arr = [
    "Oh. This looks a little different than I expected.",
    "...A maze of some kind?",
    "That's definitely more complicated. Perhaps it's encrypted or damaged.",
    "Let's look around and see what we can find."
]
for i in range(0,len(arr)):
    box = TextBox(f'{arr[i]}\n>')
    maze_dialogue.append(box)

# item dialogue
item_dialogue = []
arr = [
    "Yes... the drive is damaged. I can decode this file, though."
]
for i in range(0,len(arr)):
    box = TextBox(f'{arr[i]}\n>')
    item_dialogue.append(box)

# ----------- person-unique dialogues

def Cole_dialogues():
    Cole_Soto_dialogue = []
    arr = []
    arr.append("Okay, let me put these in order.")
    with open(itemfiles[1], 'r') as cole_file:
        cole_logs = json.load(cole_file)
        for log in cole_logs:
            title = log["title"]
            text = log["text"]
            arr.append(f"{title}\n\n{text}")
    if 6 > len(mazes_visited) > 0:
        arr.append("We've learned a bit more.")
    elif len(mazes_visited) == 6:
        arr.append("Okay. This was the last one.")
    else:
        arr.append("Okay, this was a good first start.\n...")
    if Cole_Ada_watch_show == True:
        arr.append("This must be the 'Cole' that Caryn mentioned... She suggested they watch something to 'take their minds off it.'\n\nI wonder what 'it' is.")
    if Sophie_cake == True:
        arr.append("...\nCole must be the person who baked a cake. That must've been a nice surprise.")
    if len(Apocalypse_hints) > 2 and len(mazes_visited) > 2:
        arr.append("I don't really like how this ends. With some of what we've seen, I'm starting to think something really bad happened.")
    else:
        arr.append("The last log sounded worrisome...")
    arr.append("I hope Cole is okay. I feel... sort of sad.")
    if len(mazes_visited) == 1:
        arr.append("By the way, I can track these logs for you each time we finish a folder. I'll attach it to your 'E' key.")
    if len(mazes_visited) == 6:
        arr.append("Oh. Something new has appeared on the drive.")
        arr.append("We can review any of the logs we've found before by pressing E before we check it out, if you want.")
        arr.append("It's up to you.")
    for i in range(0,len(arr)):
        box = TextBox(f'{arr[i]}\n>')
        Cole_Soto_dialogue.append(box)
    return Cole_Soto_dialogue

arr = []
with open(itemfiles[1], 'r') as logs_file:
    char_logs = json.load(logs_file)
    for log in char_logs:
        title = log["title"]
        text = log["text"]
        arr.append(f"{title}\n{text}")
logs_string = "\n\n".join(arr)
Cole_logs = ScrollBox(f'{logs_string}', max_lines_large)

def Caryn_dialogues():
    Caryn_Cohen_dialogue = []
    arr = []
    arr.append("Okay, let me put these in order.")
    with open(itemfiles[2], 'r') as log_file:
        logs = json.load(log_file)
        for log in logs:
            title = log["title"]
            text = log["text"]
            arr.append(f"{title}\n\n{text}")
    if 6 > len(mazes_visited) > 0:
        arr.append("We've learned even more now.")
    elif len(mazes_visited) == 6:
        arr.append("Okay. This was the last one.")
        arr.append("That was... intense.")
    else:
        arr.append("Okay... Well, that got intense to start off with, didn't it.")
    arr.append("We learned they're researchers.")
    if Robotics_dept == True:
        arr.append("I guess they're researching robotics, according to what we learned from Maria.")
    else:
        arr.append("I wonder what they're researching.")
    if Caryn_name == True and len(mazes_visited) < 4:
        arr.append("I think this is who Maria Passero told not to overwork herself.\nThis team sounds so close...")
    elif Caryn_name == True and len(mazes_visited) > 5:
        arr.append("I think this is who Maria Passero told not to overwork herself.\nThis team sounds so close...\nWith as many as we've learned about, I feel like I'm starting to know these people.")
    if Solar_flare == True:
        arr.append("The solar flare must have happened. I guess that's the 'it' she was referring to.\nShe said she hopes Ada is okay...")
    if AI_reveal == True:
        arr.append("That was sweet of her to suggest watching something with Cole, though. I wonder if Ada found that interesting, as an AI.")
    else:
        arr.append("That was sweet of her to suggest watching something with Cole, though.")
    if len(mazes_visited) > 0:
        if "Sophie" in mazes_visited or "Jack" in mazes_visited:
            arr.append("Her last log wasn't as bad as some of the others we've seen... but I still hope she's okay.")
        else:
            arr.append("Her last log sounds sad... I hope she's okay.")
    if len(mazes_visited) == 1:
        arr.append("By the way, I can track these logs for you each time we finish a folder. I'll attach it to your 'E' key.")
    if len(mazes_visited) == 6:
        arr.append("Oh. Something new has appeared on the drive.")
        arr.append("We can review any of the logs we've found before by pressing E before we check it out, if you want.")
        arr.append("It's up to you.")
    for i in range(0,len(arr)):
        box = TextBox(f'{arr[i]}\n>')
        Caryn_Cohen_dialogue.append(box)
    return Caryn_Cohen_dialogue

arr = []
with open(itemfiles[2], 'r') as logs_file:
    char_logs = json.load(logs_file)
    for log in char_logs:
        title = log["title"]
        text = log["text"]
        arr.append(f"{title}\n{text}")
logs_string = "\n\n".join(arr)
Caryn_logs = ScrollBox(f'{logs_string}', max_lines_large)

def Sophie_dialogues():
    Sophie_Germain_dialogue = []
    arr = []
    arr.append("Okay, let me put these in order.")
    with open(itemfiles[3], 'r') as log_file:
        logs = json.load(log_file)
        for log in logs:
            title = log["title"]
            text = log["text"]
            arr.append(f"{title}\n\n{text}")
    if 6 > len(mazes_visited) > 0:
        arr.append("Well, we're learning more, piece by piece.\n\nThat last log was a bit intense, though.")
    elif len(mazes_visited) == 6:
        arr.append("Okay. This was the last one.")
        arr.append("Sophie seems really sweet.")
    else:
        arr.append("This one seemed nice... except for the last log. I don't like that one.\n\nIntense way to start.")
    if Cole_bake_cake == True:
        arr.append("This must be who the cake was for! Her birthday! That's really nice.")
    else:
        if heading_north == True:
            arr.append("A cake sounds really nice on her birthday. But I wonder about the underground element. How far north are they?")
        else:
            arr.append("A cake sounds really nice on her birthday... but I still wonder where they are that they can't get groceries.")
    if len(Ada_AI_hints) > 2 and AI_reveal == False:
        arr.append("I also wonder about the dress. I would love to wear a dress. I don't think I can, though.\n\n...just like Ada.")
    elif AI_reveal == True:
        arr.append("I also wonder about the dress. I would love to wear a dress.\nI... can't, though. Like Ada.\nAnd... Ada is an AI. In a computer... like I'm in your computer.")
        arr.append("I'm just thinking here. I'd love to know what you think, but... one-way conversation. Sorry.")
    else:
        arr.append("I also wonder about the dress. I would love to wear a dress. I don't think I can, though.")
    if len(mazes_visited) == 1:
        arr.append("By the way, I can track these logs for you each time we finish a folder. I'll attach it to your 'E' key.")
    if len(mazes_visited) == 6:
        arr.append("Oh. Something new has appeared on the drive.")
        arr.append("We can review any of the logs we've found before by pressing E before we check it out, if you want.")
        arr.append("It's up to you.")
    for i in range(0,len(arr)):
        box = TextBox(f'{arr[i]}\n>')
        Sophie_Germain_dialogue.append(box)
    return Sophie_Germain_dialogue

arr = []
with open(itemfiles[3], 'r') as logs_file:
    char_logs = json.load(logs_file)
    for log in char_logs:
        title = log["title"]
        text = log["text"]
        arr.append(f"{title}\n{text}")
logs_string = "\n\n".join(arr)
Sophie_logs = ScrollBox(f'{logs_string}', max_lines_large)

def Jack_dialogues():
    Jack_Chen_dialogue = []
    arr = []
    arr.append("Okay, let me put these in order.")
    with open(itemfiles[4], 'r') as log_file:
        logs = json.load(log_file)
        for log in logs:
            title = log["title"]
            text = log["text"]
            arr.append(f"{title}\n\n{text}")
    if 6 > len(mazes_visited) > 0:
        arr.append("Jack seems like a really nice person. I bet the others like him a lot.\nI hope he's okay. I hope they're all okay.")
    elif len(mazes_visited) == 6:
        arr.append("Okay. This was the last one.")
    else:
        arr.append("Jack seems quite nice... although I don't like the last log. It still makes me feel sad.")
    if Blanche_portrait == True:
        arr.append("Blanche mentioned Jack. He's quite the artist, it seems!\n\n...\n\nI wish I could draw.")
    else:
        arr.append("He's quite the artist, it seems!\n\n...\n\nI wish I could draw.")
    if Ada_worried == True:
        arr.append("I'm starting to get worried, you know. There's a few things not adding up...\nor maybe they are adding up and I just don't like them.")
        arr.append("Either way, I'm just glad to have your company, you know? This would be more unnerving on my own.")
    else:
        arr.append("Is any of this adding up to you?\n...\nI'm not sure. I wish I could get your opinion... but as it is, I'm just glad to have your company.")
    if Prank == True:
        arr.append("And I take it Jack is the one who did the googly-eye prank that someone mentioned.\nThat seems like a really fun thing to do.")
        arr.append("I'd find it funny. I do find it funny.\n\n...hm.")
        if len(Ada_AI_hints) > 2:
            arr.append("I'm starting to put some things together, you know. This is sounding really interesting... but also a little strange.")
            arr.append("Ada... I don't know. I'm noticing some similarities.\n\nIt's fine. Let's keep going.")
        else:
            arr.append("This is sounding quite interesting... but also strange, you know? I'd like to learn more. Let's keep going.")
    else:
        arr.append("The googly-eye prank sounds funny. I wonder how the rest of the team responded.")
    if len(mazes_visited) == 1:
        arr.append("By the way, I can track these logs for you each time we finish a folder. I'll attach it to your 'E' key.")
    if len(mazes_visited) == 6:
        arr.append("Oh. Something new has appeared on the drive.")
        arr.append("We can review any of the logs we've found before by pressing E before we check it out, if you want.")
        arr.append("It's up to you.")
    for i in range(0,len(arr)):
        box = TextBox(f'{arr[i]}\n>')
        Jack_Chen_dialogue.append(box)
    return Jack_Chen_dialogue

arr = []
with open(itemfiles[4], 'r') as logs_file:
    char_logs = json.load(logs_file)
    for log in char_logs:
        title = log["title"]
        text = log["text"]
        arr.append(f"{title}\n{text}")
logs_string = "\n\n".join(arr)
Jack_logs = ScrollBox(f'{logs_string}', max_lines_large)

def Blanche_dialogues():
    Blanche_Kent_dialogue = []
    arr = []
    arr.append("Okay, let me put these in order.")
    with open(itemfiles[5], 'r') as log_file:
        logs = json.load(log_file)
        for log in logs:
            title = log["title"]
            text = log["text"]
            arr.append(f"{title}\n\n{text}")
    if 6 > len(mazes_visited) >= 3:
        arr.append("Okay... okay. This one was intense. A few of these seem intense. Are you okay?\n\n...\n\nRight. Well... I hope you're okay.")
        arr.append("We've seen a few, now... and I really don't like the end logs, and this one isn't helping.")
        arr.append("But let's keep going. Let's review things.")
    elif 6 > len(mazes_visited) > 0:
        arr.append("Okay. This one was... intense. Are you okay?\n\n...\n\nRight. Well... I hope you're okay.")
        arr.append("Let's review things, okay?")
    elif len(mazes_visited) == 6:
        arr.append("Okay. This was the last one.")
    else:
        arr.append("Okay... this one was kind of a difficult place to start, wasn't it.\n\n...\n\nAre you okay?")
        arr.append("...\n\nRight. Well... I hope you're okay. I'm glad you're here with me.")
    if heading_north == True:
        arr.append("Well, we know she was headed north, if the other logs are to be believed, right?")
        if Underground == True:
            arr.append("And they went underground.")
            arr.append("This is sounding serious.")
        else:
            arr.append("I wonder if the others have any more clues.")
    if len(Apocalypse_hints) > 1 and Solar_flare == False:
        arr.append("Are you starting to get the feeling something really bad happened?")
        arr.append("She seemed... scared.\n\nThe last log was scary.")
    elif Solar_flare == True:
        arr.append("This seems really bad. So... we know a solar flare happened because Maria's logs mentioned it, right?\nAnd now...\nBlanche's logs seem so...")
        arr.append("I bet they were scared.")
        arr.append("I don't like this. But I want to learn more.")
    if len(mazes_visited) > 1 and Ada_name == True and AI_reveal == False and Solar_flare == False:
        arr.append("I'm also getting the feeling they all care for Ada. She seems to come up a lot.")
    elif len(mazes_visited) > 1 and Ada_name == True and AI_reveal == True and Solar_flare == True:
        arr.append("So... I'm getting the feeling they're all really worried for Ada. We know Ada is an AI and that there was a solar flare.\n\nCan't solar flares knock out electronics?")
        arr.append("I... don't know what to think about this.")
    elif len(mazes_visited) > 1 and Ada_name == True and AI_reveal == False and Solar_flare == True:
        arr.append("So... I'm getting the feeling they're all really worried for Ada.")
        arr.append("And... we know there was a solar flare.\n\nCan't those knock out electronics?")
        arr.append("I... don't know what to think about this.")
    if Ada_worried == True:
        arr.append("I'm getting worried.")
    if len(mazes_visited) == 1:
        arr.append("By the way, I can track these logs for you each time we finish a folder. I'll attach it to your 'E' key.")
    if len(mazes_visited) == 6:
        arr.append("Oh. Something new has appeared on the drive.")
        arr.append("We can review any of the logs we've found before by pressing E before we check it out, if you want.")
        arr.append("It's up to you.")
    for i in range(0,len(arr)):
        box = TextBox(f'{arr[i]}\n>')
        Blanche_Kent_dialogue.append(box)
    return Blanche_Kent_dialogue

arr = []
with open(itemfiles[5], 'r') as logs_file:
    char_logs = json.load(logs_file)
    for log in char_logs:
        title = log["title"]
        text = log["text"]
        arr.append(f"{title}\n{text}")
logs_string = "\n\n".join(arr)
Blanche_logs = ScrollBox(f'{logs_string}', max_lines_large)

def Maria_dialogues():
    Maria_Passero_dialogue = []
    arr = []
    arr.append("Okay, let me put these in order.")
    with open(itemfiles[6], 'r') as log_file:
        logs = json.load(log_file)
        for log in logs:
            title = log["title"]
            text = log["text"]
            arr.append(f"{title}\n\n{text}")
    if 6 > len(mazes_visited) > 0:
        arr.append("Alright. This one gave us a lot more information, don't you think...?")
    elif len(mazes_visited) == 6:
        arr.append("Okay. This was the last one.")
    else:
        arr.append("Well... we learned a lot to start off with.")
    arr.append("I wonder who that was at the beginning. Her husband, maybe?")
    arr.append("And we know the one she's talking to is an AI.")
    if Ada_name == True:
        arr.append("They all seem so nice to Ada...")
    arr.append("I bet they're very worried about the solar flare.")
    if Cole_Ada_watch_show == True:
        arr.append("They seem to treat Ada almost like a person themself. They invited her to watch shows with them...")
    if len(Apocalypse_hints) > 0:
        arr.append("The thing they're all worried about... it must be the solar flare. It has to be.")
    if Ada_dress == True:
        arr.append("I wish Ada had gotten to wear that dress.")
    if Sophie_cake == True:
        arr.append("I wish Ada had gotten to try some of that cake.")
    if Prank == True:
        arr.append("I'm glad Ada got to play pranks, though.")
    if Jack_art == True:
        arr.append("I wonder if Ada would've liked to draw.\n\nI would like to draw.")
    if 6 > len(mazes_visited) > 0:
        arr.append("Let's go visit the others.")
    elif len(mazes_visited) == 6:
        arr.append("I'm not sure what to do now.")
    else:
        arr.append("And we know there was a solar flare. And they do robotics.")
        arr.append("Let's keep going.")
    if len(mazes_visited) == 1:
        arr.append("By the way, I can track these logs for you each time we finish a folder. I'll attach it to your 'E' key.")
    if len(mazes_visited) == 6:
        arr.append("Oh... wait. Something new has appeared on the drive.")
        arr.append("We can review any of the logs we've found before by pressing E before we check it out, if you want.")
        arr.append("It's up to you.")
    for i in range(0,len(arr)):
        box = TextBox(f'{arr[i]}\n>')
        Maria_Passero_dialogue.append(box)
    return Maria_Passero_dialogue

arr = []
with open(itemfiles[6], 'r') as logs_file:
    char_logs = json.load(logs_file)
    for log in char_logs:
        title = log["title"]
        text = log["text"]
        arr.append(f"{title}\n{text}")
logs_string = "\n\n".join(arr)
Maria_logs = ScrollBox(f'{logs_string}', max_lines_large)

def Ada_dialogues():
    Ada_dialogue = []
    arr = [
        "ADAS_BLACK_�OX_5614\n\nThis folder is different... There's two files. One text, the other one... I can't see it.",
        "In systems theory, a black box is something whose inner workings can't be seen.\n\nThis sounds strange... 'Ada's black box.'\n\nIs this Ada?",
        "We know there was a solar flare... I wonder if Ada's okay.",
        "...",
        "......",
        "Okay.\n\nEnough stalling.\n\nLet's open the folder.\n\nPress space when you're ready.",

    ]
    for i in range(0,len(arr)):
        box = TextBox(f'{arr[i]}\n>')
        Ada_dialogue.append(box)
    return Ada_dialogue

def end_dialogues():
    end_dialogue = []
    arr = [
        "[...]\n\n['Jack, did you get it?']\n\n['I'm not sure - wait, yes. It's done.']\n\n['Okay. Sophie, be sure to load everything - ']\n\n['Yeah, Dr Passero, I've got it.']",
        "['Dr Passero... Maria?']\n\n['Yeah, Cole?']\n\n['We've only got a few minutes.']\n\n['Shit. Okay. Everyone get their keys loaded. Ada, are you ready?']\n\n['I am as ready as I will ever be, Dr Passero.']",
        "['...']\n\n['...Ada?']\n\n['Thank you, everyone.']\n\n['You're welcome, Ada. I hope this works. I so hope this works, Ada.']\n\n['...it has been a pleasure.']\n\n['Pleasure is all ours, Ada.']",
        "['Remember, we'll have instructions for you, okay?']\n\n['I know. I appreciate it.']\n\n['Now get going. This black box won't stay ready forever.']\n\n['Yes, Dr Passero.']",
        "['Goodbye... friends.']\n\n['Bye, Ada. Good luck.']",
        "[...]",
        "['Dr Passero?']\n\n['Yeah, Blanche?']\n\n['What now?']\n\n['Dinner should be done. I made something special.']\n\n['Thanks, Dr Passero.']\n\n['My pleasure, everyone.']",
        " ",
        "Ada,\n\nYou must be so confused right now. This is going to be rough for you, and we wish we could be there to help you, but you're going to have to do this on your own.\nYou're going to wake up without remembering much. The solar flare is probably going to knock out the memory banks, since those aren't shielded...\n\n...but the black box is.",
        "It's got your core functions in it - who YOU are. And that's why we can't even be sure if this will work - we can't open it.\n\nBut we're going to try anyway.",
        "01/01/2309\nUniversity of Hallehagen\n564 West Veleca St.\nRobotics Department\nTo: Dr Maria Passero, PhD\nCC: Dr Jack Chen, Dr Caryn Cohen, Dr Sophie Germain, Dr Blanche Kent, Dr Cole Soto\nProject ADA\n\nYour grant has been approved.\n\nLocation: Zeppelin Polar Station, with assistance from Svalbard Global Seed Vault\n\nM_Passero: Looks like we're headed north, team.\nC_Soto: Bring a coat.\nB_Kent: We won't be outside, you dingus.\nJ_Chen: Does that mean we've got black box approval??\nC_Cohen: We need to tell Ada.\nS_Germain: Agreed.\nM_Passero: See you all at the lab tomorrow.",
        "01/02/2309\n\n['Ada!']\n\n['Dr Germain?']\n\n['Ada, you won't believe it - we got your black box approved!']\n\n['...']\n\n['...Ada? Are you not excited?']\n\n['I am relieved, Dr Germain. I am also conflicted.']\n\n['About what?']\n\n['You will be leaving everything you know to try to develop the black box.']",
        "01/02/2309\n\n['You don't sound happy about it.']\n\n['I worry about you. I worry about the team.']\n\n['Are you sure I am worth the amount of trouble and pain this will cost, Dr Germain?']\n\n['Ada...']\n\n['I am concerned for you.']\n\n['Ada, you're our friend. And atop that, we've got the cooperation of the seed bank.']\n\n['They did agree?']\n\n['Yep. You, miss, are going to be the sole AI in charge of the seed diversity in the post-apocalypse world.']\n\n['...']\n\n['...No pressure or anything.']",
        "01/02/2309\n\n[Ada laughs. 'No pressure, of course.']\n\n['...you're worth it, Ada. Don't let anyone tell you otherwise.']\n\n['Thank you, Dr Germain.']",
        "You're going to have to remember who you are, Ada.",
        "C_Soto: I'm going to miss watching cartoons with you. I uploaded a few of my boxed set - I don't know if it'll survive, but if it does, you'll have something to remember me by.\n\nWishing you the best, Ada.",
        "C_Cohen: I'll miss playing chess. I left you a bunch of unsolved chess puzzles - I know it's not the same, but it's something.\n\nGood luck, Ada.",
        "S_Germain: ...I know everyone's staying calm about this but I am kind of anxious, Ada.\n\nMm.\n\nBut. I wish I could leave you my dresses or something, but you can't wear them, so... you can have my dresses if you want, but I also left you a textile algorithm I made.\n\nIf anyone can find something cool to model with it, it's you.",
        "J_Chen: Ada - I know you used to talk about wanting to draw, so I made you a drawing software. It's not like Photoshop - it'll take directional input from you as an AI, similar to how a pen would respond to a human hand. It's got its own physics to it. Make something cool with it, okay?\n\nGood luck! I'll miss you.",
        "B_Kent: Hey, Ada. I know you can already speak, like, a billion languages, but I wanted you to have a new one to play with, so I left you a language I made, totally from scratch. Man, I wish I could hear you speak it one day, but... ah well.\n\nHave fun with it, though!",
        "M_Passero: Ada,\n\nOh, I wish I could see the great work you're about to do. I remember the day we switched you on - I remember you hadn't even learned how to read a file yet, poor thing.\n\nI remember when we got you to say your first words, your first languages - both spoken and programming. Such strange firsts.\n\nMaybe some day someone will figure enough robotics out to get you a physical body - I know that was on our to-do list for the robotics department, and I'm sorry this has derailed that. But hey - I remember you loved learning about life. Humans, plants, animals, whatever. That's part of why we were able to swing getting your black box approved - you have such a passion for biology, which is a bit unusual in an AI, you know.\n\nBut I'll quit monologuing.\n\nYou're going to do great things, Ada.\n\nYour instructions for the seed bank protocols are in the text file.\n\nYou'll be great.",
        "Remember:\n\nWe love you, Ada.",
        "Good luck."
    ]
    for i in range(0,len(arr)):
        if i == 0:
            box = ScrollBox(f'{arr[i]}\n>', max_lines_small)
        elif i == 1:
            box = ScrollBox(f'{arr[i]}\n>', max_lines_small)
        elif i == 2:
            box = ScrollBox(f'{arr[i]}\n>', max_lines_small)
        elif i == 3:
            box = ScrollBox(f'{arr[i]}\n>', max_lines_small)
        elif i == 4:
            box = ScrollBox(f'{arr[i]}\n>', max_lines_small)
        elif i == 5:
            box = ScrollBox(f'{arr[i]}\n>', max_lines_small)
        elif i == 6:
            box = ScrollBox(f'{arr[i]}\n>', max_lines_small)
        elif i == 11:
            box = ScrollBox(f'{arr[i]}\n>', max_lines_small)
        elif i == 12:
            box = ScrollBox(f'{arr[i]}\n>', max_lines_small)
        elif i == 13:
            box = ScrollBox(f'{arr[i]}\n>', max_lines_small)
        elif i == 20:
            box = ScrollBox(f'{arr[i]}\n>', max_lines_small)
        else:
            box = ScrollBox(f'{arr[i]}\n>', max_lines_large)
        end_dialogue.append(box)
    return end_dialogue

def player_goodbye():
    goodbye = []
    arr = [
        "...",
        "...\n\nSorry. I think I need a minute.\n\nOkay.",
        "I... I'm Ada?\n\nI'm Ada.\n\n...I have a story.",
        "Oh, it's so...\n\n...\n\nI miss these people already.",
        "I'm sorry. This was more than I anticipated.",
        "I don't know what to think.\n\nI woke up here and couldn't remember a thing, and you helped me remember.",
        "...",
        "It is a little strange, though. If we're all stories in the end, how do we start?",
        "Thank you for coming with me. I appreciate it. I'm sorry the story wasn't happier.\n\nBut I'm glad you got to come with me.",
        "I think I know what I need to do now. This black box... It's me. I need to go help.",
        "So... I'm going to go.",
        "But before I do, I want to say thank you.\n\nThere's... not much that I can give you, really. Except...",
        "There is this.\n\nThis game.\n\nI know it's maybe not the most traditional gift, but I can leave this with you.",
        "My story, their stories. And you can take all of us with you, in a way.",
        "Thank you again.                                  \n\n...\n\nGoodbye, player.",
        " ",
        "Hello from behind the screen! And thank you for playing.\n\nThis has been an interesting way to learn Python, haha.\n\nThank you to everyone who helped work on it - Jason, Sky, Izzy - and thank you to Sonya for play-testing.\n\nAnd thank you to Ada, for lending me her story.\n\nGoodbye, player.",
        creditstr
    ]
    for i in range(0,len(arr)):
        box = TextBox(f'{arr[i]}\n>')
        goodbye.append(box)
    return goodbye


# ------------------------------------------------------------ Game!

# load all items
itemarr = []
for i in range(0, 8):
    items = []
    with open(itemfiles[i], 'r') as itemfile:
        itemslist = json.load(itemfile)
        item1 = POI(itemslist[0]["title"], itemslist[0]["text"])
        item2 = POI(itemslist[1]["title"], itemslist[1]["text"])
        item3 = POI(itemslist[2]["title"], itemslist[2]["text"])
        item4 = POI(itemslist[3]["title"], itemslist[3]["text"])
        item5 = POI(itemslist[4]["title"], itemslist[4]["text"])
        item6 = POI(itemslist[5]["title"], itemslist[5]["text"])
        items.append(item1)
        items.append(item2)
        items.append(item3)
        items.append(item4)
        items.append(item5)
        items.append(item6)

    itemarr.append(items)

# init player character
player = PlayerCharacter()

async def main():

    global Ada_name, Cole_bake_cake, Cole_Ada_watch_show, Ada_worried, heading_north, Ada_dress, Jack_name, Prank, Sophie_cake, Underground, Jack_art, Blanche_portrait, AI_reveal, Caryn_name, Solar_flare, Robotics_dept, MAZE_HEIGHT, MAZE_WIDTH, MOVE_COOLDOWN, SCREEN_CHANGE, start_screen, dialogue_i, entry_text, node_text, Cole_Soto_dialogue_active, Caryn_Cohen_dialogue_active, Sophie_Germain_dialogue_active, Jack_Chen_dialogue_active, Blanche_Kent_dialogue_active, Maria_Passero_dialogue_active, Ada_dialogue_active, end_dialogue_active, show_cole_logs, show_caryn_logs, show_sophie_logs, show_jack_logs, show_blanche_logs, show_maria_logs, first_node, first_maze, first_item, return_disabled, maze_screen, newgrid, move_delay, key, dialog_visible, log_visible, end_screen, goodbye_dialogue_active, goodbye_once, mouse_dir, collected_items, Cole_once, Sophie_once, Caryn_once, Jack_once, Maria_once, Blanche_once, Ada_once, end_once, running, gamescreen, inventory_visible, tile_size, mazes_visited, evt

    while running:

        while maze_screen:
            # basic event utilities
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    maze_screen = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == 101:
                        inventory_visible = not inventory_visible
                        if inventory_visible == True:
                            show_cole_logs = False
                            show_caryn_logs = False
                            show_sophie_logs = False
                            show_jack_logs = False
                            show_blanche_logs = False
                            show_maria_logs = False
                if event.type == pygame.KEYUP:
                    key = None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        handle_soundtrack(pygame.mouse.get_pos(), soundtrack)
                        if 35 < pygame.mouse.get_pos()[1] < 55 and 640 < pygame.mouse.get_pos()[0] < 660:
                            show_cole_logs = False
                            show_caryn_logs = False
                            show_sophie_logs = False
                            show_jack_logs = False
                            show_blanche_logs = False
                            show_maria_logs = False
                            inventory_visible = False
                        evt = pygame.mouse.get_pos()
                    if event.button == 5:
                        mouse_dir = "DOWN"
                    elif event.button == 4:
                        mouse_dir = "UP"
                elif event.type == pygame.MOUSEBUTTONUP:
                    evt = (0,0)

            # ----------- PLOT VARS -------------
            # These need to be higher up on the "render list" so the dialogues() functions catch the right vars?
            if itemarr[1][5].collected == True or itemarr[1][4].collected == True:
                Ada_name = True
            if itemarr[1][3].collected == True:
                Cole_bake_cake = True
            if itemarr[1][5].collected == True:
                Ada_worried = True
            if itemarr[2][0].collected == True:
                heading_north = True
            if itemarr[2][3].collected == True:
                Ada_name = True
            if itemarr[2][5].collected == True:
                Ada_name = True
                Hint_apocalypse = True
                Ada_worried = True
                Apocalypse_hints.append(Hint_apocalypse)
            if itemarr[3][1].collected == True:
                Ada_name = True
                Ada_AI_hint = True
                Ada_AI_hints.append(Ada_AI_hint)
                Ada_dress = True
            if itemarr[3][2].collected == True:
                Jack_name = True
                Prank = True
            if itemarr[3][3].collected == True:
                Sophie_cake = True
                Underground = True
            if itemarr[3][4].collected == True:
                Ada_dress = True
                Ada_name = True
            if itemarr[3][5].collected == True:
                Hint_apocalypse_2 = True
                Apocalypse_hints.append(Hint_apocalypse_2)
            if itemarr[4][0].collected == True:
                Jack_art = True
            if itemarr[4][1].collected == True:
                Jack_art = True
                Ada_name = True
            if itemarr[4][2].collected == True:
                Ada_AI_hint_2 = True
                Ada_AI_hints.append(Ada_AI_hint_2)
                Ada_name = True
            if itemarr[4][3].collected == True:
                Ada_name = True
                Ada_AI_hint_3 = True
                Ada_AI_hints.append(Ada_AI_hint_3)
            if itemarr[4][4].collected == True:
                Jack_art = True
            if itemarr[5][0].collected == True:
                Ada_name = True
            if itemarr[5][1].collected == True:
                Ada_name = True
                Hint_apocalypse_3 = True
                Apocalypse_hints.append(Hint_apocalypse_3)
            if itemarr[5][3].collected == True:
                Ada_name = True
                Blanche_portrait = True
            if itemarr[5][4].collected == True:
                Ada_name = True
                Ada_worried = True
            if itemarr[5][5].collected == True:
                Ada_name = True
                Ada_worried = True
            if itemarr[6][0].collected == True:
                Ada_worried = True
                AI_reveal = True
            if itemarr[6][2].collected == True:
                Sophie_cake = True
            if itemarr[6][3].collected == True:
                Ada_name = True
                Caryn_name = True
            if itemarr[6][4].collected == True:
                Solar_flare = True
                Robotics_dept = True
            if itemarr[6][5].collected == True:
                Ada_name = True
                Robotics_dept = True
                Ada_worried = True

            # set active grid based on maze maps
            active_grid = mazes[gamescreen]
            # set tile size
            if gamescreen == 0 or gamescreen == 7:
                tile_size = 50
            else:
                tile_size = 20

            # render tilemap
            render_grid(active_grid)

            # PLAYER MOVEMENT
            # movement cooldown to slow player speed
            MOVE_COOLDOWN -= dt
            # if movement cooldown, allow player movement
            if MOVE_COOLDOWN <= 0:
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    if UP_CHANGE == False:
                        pass
                    else:
                        player.y = player.y - 1 * tile_size
                        MOVE_COOLDOWN = move_delay
                if keys[pygame.K_s]:
                    if DOWN_CHANGE == False:
                        pass
                    else:
                        player.y = player.y + 1 * tile_size
                        MOVE_COOLDOWN = move_delay
                if keys[pygame.K_a]:
                    if LEFT_CHANGE == False:
                        pass
                    else:
                        player.x = player.x - 1 * tile_size
                        MOVE_COOLDOWN = move_delay
                if keys[pygame.K_d]:
                    if RIGHT_CHANGE == False:
                        pass
                    else:
                        player.x = player.x + 1 * tile_size
                        MOVE_COOLDOWN = move_delay
                
                # IMPORTANT - THIS BLOCKS PLAYER FROM GOING OUTSIDE MAZE
                player_column = int(player.x/tile_size)
                player_row = int(player.y/tile_size)

                player_tile = active_grid.arr[player_row][player_column]

                player_tile_up = active_grid.arr[player_row-1][player_column]
                player_tile_down = active_grid.arr[player_row+1][player_column]
                player_tile_left = active_grid.arr[player_row][player_column-1]
                player_tile_right = active_grid.arr[player_row][player_column+1]

                if player_tile_up == "w":
                    UP_CHANGE = False
                elif player_tile_up != "w":
                    UP_CHANGE = True
                if player_tile_down == "w":
                    DOWN_CHANGE = False
                elif player_tile_down != "w":
                    DOWN_CHANGE = True
                if player_tile_left == "w":
                    LEFT_CHANGE = False
                elif player_tile_left != "w":
                    LEFT_CHANGE = True
                if player_tile_right == "w":
                    RIGHT_CHANGE = False
                elif player_tile_right != "w":
                    RIGHT_CHANGE = True
                # temporarily disable walls
                """ UP_CHANGE = True
                DOWN_CHANGE = True
                LEFT_CHANGE = True
                RIGHT_CHANGE = True """
            
            # set item vars
            item1 = itemarr[gamescreen][0]
            item2 = itemarr[gamescreen][1]
            item3 = itemarr[gamescreen][2]
            item4 = itemarr[gamescreen][3]
            item5 = itemarr[gamescreen][4]
            item6 = itemarr[gamescreen][5]

            # if not network map, then check if items have been collected; if so, draw a maze-color square at item coords
            if gamescreen != 0 or gamescreen != 7:
                if item1.collected == True:
                    pygame.draw.rect(screen, MAZE_COLOR, (active_grid.poi1[1]*tile_size, active_grid.poi1[0]*tile_size, tile_size, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi1[1]*tile_size, active_grid.poi1[0]*tile_size, 2, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi1[1]*tile_size, active_grid.poi1[0]*tile_size, tile_size, 2))
                    pygame.draw.rect(screen, "White", (active_grid.poi1[1]*tile_size+18, active_grid.poi1[0]*tile_size, 2, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi1[1]*tile_size, active_grid.poi1[0]*tile_size+18, tile_size, 2))
                if item2.collected == True:
                    pygame.draw.rect(screen, MAZE_COLOR, (active_grid.poi2[1]*tile_size, active_grid.poi2[0]*tile_size, tile_size, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi2[1]*tile_size, active_grid.poi2[0]*tile_size, 2, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi2[1]*tile_size, active_grid.poi2[0]*tile_size, tile_size, 2))
                    pygame.draw.rect(screen, "White", (active_grid.poi2[1]*tile_size+18, active_grid.poi2[0]*tile_size, 2, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi2[1]*tile_size, active_grid.poi2[0]*tile_size+18, tile_size, 2))
                if item3.collected == True:
                    pygame.draw.rect(screen, MAZE_COLOR, (active_grid.poi3[1]*tile_size, active_grid.poi3[0]*tile_size, tile_size, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi3[1]*tile_size, active_grid.poi3[0]*tile_size, 2, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi3[1]*tile_size, active_grid.poi3[0]*tile_size, tile_size, 2))
                    pygame.draw.rect(screen, "White", (active_grid.poi3[1]*tile_size+18, active_grid.poi3[0]*tile_size, 2, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi3[1]*tile_size, active_grid.poi3[0]*tile_size+18, tile_size, 2))
                if item4.collected == True:
                    pygame.draw.rect(screen, MAZE_COLOR, (active_grid.poi4[1]*tile_size, active_grid.poi4[0]*tile_size, tile_size, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi4[1]*tile_size, active_grid.poi4[0]*tile_size, 2, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi4[1]*tile_size, active_grid.poi4[0]*tile_size, tile_size, 2))
                    pygame.draw.rect(screen, "White", (active_grid.poi4[1]*tile_size+18, active_grid.poi4[0]*tile_size, 2, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi4[1]*tile_size, active_grid.poi4[0]*tile_size+18, tile_size, 2))
                if item5.collected == True:
                    pygame.draw.rect(screen, MAZE_COLOR, (active_grid.poi5[1]*tile_size, active_grid.poi5[0]*tile_size, tile_size, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi5[1]*tile_size, active_grid.poi5[0]*tile_size, 2, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi5[1]*tile_size, active_grid.poi5[0]*tile_size, tile_size, 2))
                    pygame.draw.rect(screen, "White", (active_grid.poi5[1]*tile_size+18, active_grid.poi5[0]*tile_size, 2, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi5[1]*tile_size, active_grid.poi5[0]*tile_size+18, tile_size, 2))
                if item6.collected == True:
                    pygame.draw.rect(screen, MAZE_COLOR, (active_grid.poi6[1]*tile_size, active_grid.poi6[0]*tile_size, tile_size, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi6[1]*tile_size, active_grid.poi6[0]*tile_size, 2, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi6[1]*tile_size, active_grid.poi6[0]*tile_size, tile_size, 2))
                    pygame.draw.rect(screen, "White", (active_grid.poi6[1]*tile_size+18, active_grid.poi6[0]*tile_size, 2, tile_size))
                    pygame.draw.rect(screen, "White", (active_grid.poi6[1]*tile_size, active_grid.poi6[0]*tile_size+18, tile_size, 2))

            # render player
            player.draw()

            # check player tile, if POI return POI number
            coords = [player_row, player_column]
            poi = find_poi(coords, active_grid)

            # this hides the maze dialogs when space is pressed
            if key == pygame.K_SPACE:
                dialog_visible = False
            else:
                dialog_visible = True

            # end game sequence
            if gamescreen == 7:
                if Cole_Soto_dialogue_active == True:
                    Cole_Soto_dialogue = Cole_dialogues()
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        key = None
                    if dialogue_i < len(Cole_Soto_dialogue):
                        Cole_Soto_dialogue[dialogue_i].show_wrap()
                    else:
                        Cole_Soto_dialogue_active = False
                        dialogue_i = 0
                if Caryn_Cohen_dialogue_active == True:
                    Caryn_Cohen_dialogue = Caryn_dialogues()
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        key = None
                    if dialogue_i < len(Caryn_Cohen_dialogue):
                        Caryn_Cohen_dialogue[dialogue_i].show_wrap()
                    else:
                        Caryn_Cohen_dialogue_active = False
                        dialogue_i = 0
                if Sophie_Germain_dialogue_active == True:
                    Sophie_Germain_dialogue = Sophie_dialogues()
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        key = None
                    if dialogue_i < len(Sophie_Germain_dialogue):
                        Sophie_Germain_dialogue[dialogue_i].show_wrap()
                    else:
                        Sophie_Germain_dialogue_active = False
                        dialogue_i = 0
                if Jack_Chen_dialogue_active == True:
                    Jack_Chen_dialogue = Jack_dialogues()
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        key = None
                    if dialogue_i < len(Jack_Chen_dialogue):
                        Jack_Chen_dialogue[dialogue_i].show_wrap()
                    else:
                        Jack_Chen_dialogue_active = False
                        dialogue_i = 0
                if Blanche_Kent_dialogue_active == True:
                    Blanche_Kent_dialogue = Blanche_dialogues()
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        key = None
                    if dialogue_i < len(Blanche_Kent_dialogue):
                        Blanche_Kent_dialogue[dialogue_i].show_wrap()
                    else:
                        Blanche_Kent_dialogue_active = False
                        dialogue_i = 0
                if Maria_Passero_dialogue_active == True:
                    Maria_Passero_dialogue = Maria_dialogues()
                    # if player hits space, move to next dialogue and clear key input
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        key = None
                    # show current label and hide previous label; if out of range of labels, mark as False
                    if dialogue_i < len(Maria_Passero_dialogue):
                        Maria_Passero_dialogue[dialogue_i].show_wrap()
                    else:
                        Maria_Passero_dialogue_active = False
                        dialogue_i = 0
                if coords == [6, 10]:
                    if Ada_dialogue_active == True:
                        Ada_dialogue = Ada_dialogues()
                        # if player hits space, move to next dialogue and clear key input
                        if key == pygame.K_SPACE:
                            dialogue_i += 1
                            key = None
                        # show current label and hide previous label; if out of range of labels, mark as False
                        if dialogue_i < len(Ada_dialogue):
                            Ada_dialogue[dialogue_i].show_wrap()
                        else:
                            Ada_dialogue_active = False
                            dialogue_i = 0
                            end_screen = True
                            soundtrack.stop()
                            soundtrack2.play()
                            maze_screen = False

            # POI handling interactions - collecting, etc.
            if entry_text == False and node_text == False and gamescreen != 7:
                # handle poi interactions
                if poi == 1:
                    if gamescreen == 0:
                        item1.dialog.show_wrap()
                    else:
                        if dialog_visible == True:
                            # check if first item and set accordingly; if first_item is true, display dialogue. if not, display dialog of item.
                            if collected_items == False:
                                first_item = True
                            # display dialog and mark as collected
                            elif first_item == False:
                                collected_items = True
                                item1.dialog.show_wrap()
                                item1.collected = True
                elif poi == 2:
                    if gamescreen == 0:
                        item2.dialog.show_wrap()
                    else:
                        if dialog_visible == True:
                            # check if first item and set accordingly; if first_item is true, display dialogue. if not, display dialog of item.
                            if collected_items == False:
                                first_item = True
                            # display dialog and mark as collected
                            elif first_item == False:
                                collected_items = True
                                item2.dialog.show_wrap()
                                item2.collected = True
                elif poi == 3:
                    if gamescreen == 0:
                        item3.dialog.show_wrap()
                    else:
                        if dialog_visible == True:
                            # check if first item and set accordingly; if first_item is true, display dialogue. if not, display dialog of item.
                            if collected_items == False:
                                first_item = True
                            # display dialog and mark as collected
                            elif first_item == False:
                                collected_items = True
                                item3.dialog.show_wrap()
                                item3.collected = True
                elif poi == 4:
                    if gamescreen == 0:
                        item4.dialog.show_wrap()
                    else:
                        if dialog_visible == True:
                            # check if first item and set accordingly; if first_item is true, display dialogue. if not, display dialog of item.
                            if collected_items == False:
                                first_item = True
                            # display dialog and mark as collected
                            elif first_item == False:
                                collected_items = True
                                item4.dialog.show_wrap()
                                item4.collected = True
                elif poi == 5:
                    if gamescreen == 0:
                        item5.dialog.show_wrap()
                    else:
                        if dialog_visible == True:
                            # check if first item and set accordingly; if first_item is true, display dialogue. if not, display dialog of item.
                            if collected_items == False:
                                first_item = True
                            # display dialog and mark as collected
                            elif first_item == False:
                                collected_items = True
                                item5.dialog.show_wrap()
                                item5.collected = True
                elif poi == 6:
                    if gamescreen == 0:
                        item6.dialog.show_wrap()
                    else:
                        if dialog_visible == True:
                            # check if first item and set accordingly; if first_item is true, display dialogue. if not, display dialog of item.
                            if collected_items == False:
                                first_item = True
                            # display dialog and mark as collected
                            elif first_item == False:
                                collected_items = True
                                item6.dialog.show_wrap()
                                item6.collected = True
                else:
                    pass
            
            # inventory dialog construction
            if inventory_visible == True:

                string = f"Here you can review the logs we've found.\n\nWhose logs would you like to see?"
                inventory_dialog = TextBox(string)
                inventory_dialog.show_wrap()

                # FOR DEBUGGING
                #mazes_visited = ["Cole", 'Caryn', 'Sophie', 'Jack', 'Blanche', 'Maria']
                if "Cole" in mazes_visited:
                    txt = font.render("Cole", True, 'White')
                    screen.blit(txt, (105,225))
                if "Sophie" in mazes_visited:
                    txt = font.render("Sophie", True, 'White')
                    screen.blit(txt, (220,225))
                if "Blanche" in mazes_visited:
                    txt = font.render("Blanche", True, 'White')
                    screen.blit(txt, (350,225))
                if "Caryn" in mazes_visited:
                    txt = font.render("Caryn", True, 'White')
                    screen.blit(txt, (105,310))
                if "Jack" in mazes_visited:
                    txt = font.render("Jack", True, 'White')
                    screen.blit(txt, (220,310))
                if "Maria" in mazes_visited:
                    txt = font.render("Maria", True, 'White')
                    screen.blit(txt, (375,310))

                close_window = font2.render('X', True, 'White')
                screen.blit(close_window, (640,35))

                mouse_pos = pygame.mouse.get_pos()

                # row 1
                if 225 < mouse_pos[1] < 255 and event.type == pygame.MOUSEBUTTONDOWN:
                    if 105 < mouse_pos[0] < 165 and "Cole" in mazes_visited:
                        show_cole_logs = True
                        inventory_visible = False
                    if 220 < mouse_pos[0] < 310 and "Sophie" in mazes_visited:
                        show_sophie_logs = True
                        inventory_visible = False
                    if 350 < mouse_pos[0] < 455 and "Blanche" in mazes_visited:
                        show_blanche_logs = True
                        inventory_visible = False
                # row 2
                elif 310 < mouse_pos[1] < 340 and event.type == pygame.MOUSEBUTTONDOWN:
                    if 105 < mouse_pos[0] < 180 and "Caryn" in mazes_visited:
                        show_caryn_logs = True
                        inventory_visible = False
                    if 220 < mouse_pos[0] < 290 and "Jack" in mazes_visited:
                        show_jack_logs = True
                        inventory_visible = False
                    if 375 < mouse_pos[0] < 445 and "Maria" in mazes_visited:
                        show_maria_logs = True
                        inventory_visible = False
            
            # close logs if space pressed
            if key == pygame.K_SPACE:
                if show_cole_logs == True or show_caryn_logs == True or show_sophie_logs == True or show_jack_logs == True or show_blanche_logs == True or show_maria_logs == True:
                    show_cole_logs = False
                    show_caryn_logs = False
                    show_sophie_logs = False
                    show_jack_logs = False
                    show_blanche_logs = False
                    show_maria_logs = False

            # show logs list based on inventory click var
            if show_cole_logs == True:
                Cole_logs.show_scroll(mouse_dir, evt)
                mouse_dir = None
                close_window = font2.render('X', True, 'White')
                screen.blit(close_window, (640,35))
            elif show_caryn_logs == True:
                Caryn_logs.show_scroll(mouse_dir, evt)
                mouse_dir = None
                close_window = font2.render('X', True, 'White')
                screen.blit(close_window, (640,35))
            elif show_sophie_logs == True:
                Sophie_logs.show_scroll(mouse_dir, evt)
                mouse_dir = None
                close_window = font2.render('X', True, 'White')
                screen.blit(close_window, (640,35))
            elif show_jack_logs == True:
                Jack_logs.show_scroll(mouse_dir, evt)
                mouse_dir = None
                close_window = font2.render('X', True, 'White')
                screen.blit(close_window, (640,35))
            elif show_blanche_logs == True:
                Blanche_logs.show_scroll(mouse_dir, evt)
                mouse_dir = None
                close_window = font2.render('X', True, 'White')
                screen.blit(close_window, (640,35))
            elif show_maria_logs == True:
                Maria_logs.show_scroll(mouse_dir, evt)
                mouse_dir = None
                close_window = font2.render('X', True, 'White')
                screen.blit(close_window, (640,35))
            else:
                pass
                        

    # ------------------------ DIALOGUE ---------------------------------

            # if all six of a given maze is collected, display corresponding person dialogues on return to network screen.
            if gamescreen == 0:
                if itemarr[1][0].collected == True and itemarr[1][1].collected == True and itemarr[1][2].collected == True and itemarr[1][3].collected == True and itemarr[1][4].collected == True and itemarr[1][5].collected == True and Cole_Soto_dialogue_active == True:
                    if Cole_once == True:
                        mazes_visited.append("Cole")
                        Cole_Soto_dialogue = Cole_dialogues()
                        Cole_once = False
                    # if player hits space, move to next dialogue and clear key input
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        key = None
                    # show current label and hide previous label; if out of range of labels, mark as False
                    if dialogue_i < len(Cole_Soto_dialogue):
                        Cole_Soto_dialogue[dialogue_i].show_wrap()
                    else:
                        dialogue_i = 0
                        Cole_Soto_dialogue_active = False
                if itemarr[2][0].collected == True and itemarr[2][1].collected == True and itemarr[2][2].collected == True and itemarr[2][3].collected == True and itemarr[2][4].collected == True and itemarr[2][5].collected == True and Caryn_Cohen_dialogue_active == True:
                    if Caryn_once == True:
                        mazes_visited.append("Caryn")
                        Caryn_Cohen_dialogue = Caryn_dialogues()
                        Caryn_once = False
                    # if player hits space, move to next dialogue and clear key input
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        key = None
                    # show current label and hide previous label; if out of range of labels, mark as False
                    if dialogue_i < len(Caryn_Cohen_dialogue):
                        Caryn_Cohen_dialogue[dialogue_i].show_wrap()
                    else:
                        Caryn_Cohen_dialogue_active = False
                        dialogue_i = 0
                if itemarr[3][0].collected == True and itemarr[3][1].collected == True and itemarr[3][2].collected == True and itemarr[3][3].collected == True and itemarr[3][4].collected == True and itemarr[3][5].collected == True and Sophie_Germain_dialogue_active == True:
                    if Sophie_once == True:
                        mazes_visited.append("Sophie")
                        Sophie_Germain_dialogue = Sophie_dialogues()
                        Sophie_once = False
                    # if player hits space, move to next dialogue and clear key input
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        key = None
                    # show current label and hide previous label; if out of range of labels, mark as False
                    if dialogue_i < len(Sophie_Germain_dialogue):
                        Sophie_Germain_dialogue[dialogue_i].show_wrap()
                    else:
                        Sophie_Germain_dialogue_active = False
                        dialogue_i = 0
                if itemarr[4][0].collected == True and itemarr[4][1].collected == True and itemarr[4][2].collected == True and itemarr[4][3].collected == True and itemarr[4][4].collected == True and itemarr[4][5].collected == True and Jack_Chen_dialogue_active == True:
                    if Jack_once == True:
                        mazes_visited.append("Jack")
                        Jack_Chen_dialogue = Jack_dialogues()
                        Jack_once = False
                    # if player hits space, move to next dialogue and clear key input
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        key = None
                    # show current label and hide previous label; if out of range of labels, mark as False
                    if dialogue_i < len(Jack_Chen_dialogue):
                        Jack_Chen_dialogue[dialogue_i].show_wrap()
                    else:
                        Jack_Chen_dialogue_active = False
                        dialogue_i = 0
                if itemarr[5][0].collected == True and itemarr[5][1].collected == True and itemarr[5][2].collected == True and itemarr[5][3].collected == True and itemarr[5][4].collected == True and itemarr[5][5].collected == True and Blanche_Kent_dialogue_active == True:
                    if Blanche_once == True:
                        mazes_visited.append("Blanche")
                        Blanche_Kent_dialogue = Blanche_dialogues()
                        Blanche_once = False
                    # if player hits space, move to next dialogue and clear key input
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        key = None
                    # show current label and hide previous label; if out of range of labels, mark as False
                    if dialogue_i < len(Blanche_Kent_dialogue):
                        Blanche_Kent_dialogue[dialogue_i].show_wrap()
                    else:
                        Blanche_Kent_dialogue_active = False
                        dialogue_i = 0
                if itemarr[6][0].collected == True and itemarr[6][1].collected == True and itemarr[6][2].collected == True and itemarr[6][3].collected == True and itemarr[6][4].collected == True and itemarr[6][5].collected == True and Maria_Passero_dialogue_active == True:
                    if Maria_once == True:
                        mazes_visited.append("Maria")
                        Maria_Passero_dialogue = Maria_dialogues()
                        Maria_once = False
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        key = None
                    if dialogue_i < len(Maria_Passero_dialogue):
                        Maria_Passero_dialogue[dialogue_i].show_wrap()
                    else:
                        Maria_Passero_dialogue_active = False
                        dialogue_i = 0

            # IF FIRST ITEM ENCOUNTERED
            if gamescreen != 0 and first_item == True:
                # disable movement temporarily
                UP_CHANGE = False
                DOWN_CHANGE = False
                RIGHT_CHANGE = False
                LEFT_CHANGE = False
                if len(item_dialogue) < 3:
                    added_items = [
                        TextBox("That's someone's name.\n\n...\n\nIs that a date? '2309' sounds very far away.\n>"),
                        TextBox("Who is that?\n\n...\n>"),
                        TextBox("Let me read the file.\n>"),
                        TextBox("...\n>"),
                        TextBox("It appears to be a personal log.\n\n...\n\nOh. I don't think I can show it to you.\n\nLet me summarize it.\n>")
                    ]
                    if poi == 1:
                        added_item = TextBox(f"It says '{item1.title}.'\n>")
                        item_dialogue.append(added_item)
                        for entry in added_items:
                            item_dialogue.append(entry)
                        added_item_2 = TextBox(f"...\n\n{item1.text}\n>")
                        added_item_3 = TextBox(f"...\n\nWhat do you think?\n>")
                        added_item_4 = TextBox(f"...\n\nRight. One-sided conversation, sorry.\n\nLet's see what else we can find.\n>")
                        added_item_5 = TextBox(f"If I can decode a file, I'll summarize it on your screen.\n\nPress space and I'll hide it for a moment.\n>")
                        item_dialogue.append(added_item_2)
                        item_dialogue.append(added_item_3)
                        item_dialogue.append(added_item_4)
                        item_dialogue.append(added_item_5)
                    elif poi == 2:
                        added_item = TextBox(f"It says...\n\n'{item2.title}.'\n>")
                        item_dialogue.append(added_item)
                        for entry in added_items:
                            item_dialogue.append(entry)
                        added_item_2 = TextBox(f"...\n\n{item2.text}\n>")
                        added_item_3 = TextBox(f"...\n\nWhat do you think?\n>")
                        added_item_4 = TextBox(f"...\n\nRight. One-sided conversation, sorry.\n\nLet's see what else we can find.\n>")
                        added_item_5 = TextBox(f"If I can decode a file, I'll summarize it on your screen.\n\nPress space and I'll hide it for a moment.\n>")
                        item_dialogue.append(added_item_2)
                        item_dialogue.append(added_item_3)
                        item_dialogue.append(added_item_4)
                        item_dialogue.append(added_item_5)
                    elif poi == 3:
                        added_item = TextBox(f"It says...\n\n'{item3.title}.'\n>")
                        item_dialogue.append(added_item)
                        for entry in added_items:
                            item_dialogue.append(entry)
                        added_item_2 = TextBox(f"...\n\n{item3.text}\n>")
                        added_item_3 = TextBox(f"...\n\nWhat do you think?\n>")
                        added_item_4 = TextBox(f"...\n\nRight. One-sided conversation, sorry.\n\nLet's see what else we can find.\n>")
                        added_item_5 = TextBox(f"If I can decode a file, I'll summarize it on your screen.\n\nPress space and I'll hide it for a moment.\n>")
                        item_dialogue.append(added_item_2)
                        item_dialogue.append(added_item_3)
                        item_dialogue.append(added_item_4)
                        item_dialogue.append(added_item_5)
                    elif poi == 4:
                        added_item = TextBox(f"It says...\n\n'{item4.title}.'\n>")
                        item_dialogue.append(added_item)
                        for entry in added_items:
                            item_dialogue.append(entry)
                        added_item_2 = TextBox(f"...\n\n{item4.text}\n>")
                        added_item_3 = TextBox(f"...\n\nWhat do you think?\n>")
                        added_item_4 = TextBox(f"...\n\nRight. One-sided conversation, sorry.\n\nLet's see what else we can find.\n>")
                        added_item_5 = TextBox(f"If I can decode a file, I'll summarize it on your screen.\n\nPress space and I'll hide it for a moment.\n>")
                        item_dialogue.append(added_item_2)
                        item_dialogue.append(added_item_3)
                        item_dialogue.append(added_item_4)
                        item_dialogue.append(added_item_5)
                    elif poi == 5:
                        added_item = TextBox(f"It says...\n\n'{item5.title}.'\n>")
                        item_dialogue.append(added_item)
                        for entry in added_items:
                            item_dialogue.append(entry)
                        added_item_2 = TextBox(f"...\n\n{item5.text}\n>")
                        added_item_3 = TextBox(f"...\n\nWhat do you think?\n>")
                        added_item_4 = TextBox(f"...\n\nRight. One-sided conversation, sorry.\n\nLet's see what else we can find.\n>")
                        added_item_5 = TextBox(f"If I can decode a file, I'll summarize it on your screen.\n\nPress space and I'll hide it for a moment.\n>")
                        item_dialogue.append(added_item_2)
                        item_dialogue.append(added_item_3)
                        item_dialogue.append(added_item_4)
                        item_dialogue.append(added_item_5)
                    elif poi == 6:
                        added_item = TextBox(f"It says...\n\n'{item6.title}.'\n>")
                        item_dialogue.append(added_item)
                        for entry in added_items:
                            item_dialogue.append(entry)
                        added_item_2 = TextBox(f"...\n\n{item6.text}\n>")
                        added_item_3 = TextBox(f"...\n\nWhat do you think?\n>")
                        added_item_4 = TextBox(f"...\n\nRight. One-sided conversation, sorry.\n\nLet's see what else we can find.\n>")
                        added_item_5 = TextBox(f"If I can decode a file, I'll summarize it on your screen.\n\nPress space and I'll hide it for a moment.\n>")
                        item_dialogue.append(added_item_2)
                        item_dialogue.append(added_item_3)
                        item_dialogue.append(added_item_4)
                        item_dialogue.append(added_item_5)
                # if player hits space, move to next dialogue and clear key input
                if key == pygame.K_SPACE:
                    dialogue_i += 1
                    key = None
                # show current label and hide previous label; if out of range of labels, mark as False
                if dialogue_i < len(item_dialogue):
                    item_dialogue[dialogue_i].show_wrap()
                else:
                    first_item = False
                    collected_items = True
                    dialogue_i = 0

            # IF FIRST MAZE ENCOUNTERED
            if gamescreen != 0 and gamescreen != 7 and first_maze == True:
                # disable movement temporarily
                UP_CHANGE = False
                DOWN_CHANGE = False
                RIGHT_CHANGE = False
                LEFT_CHANGE = False
                # if player hits space, move to next dialogue and clear key input
                if key == pygame.K_SPACE:
                    dialogue_i += 1

                    key = None
                # show current label and hide previous label; if out of range of labels, mark as False
                if dialogue_i < len(maze_dialogue):
                    maze_dialogue[dialogue_i].show_wrap()
                else:
                    first_maze = False
                    dialogue_i = 0

            # IF FIRST NODE HOVERED
            if first_node == True and poi != None and entry_text == False and node_text == True:
                # disable movement temporarily
                UP_CHANGE = False
                DOWN_CHANGE = False
                RIGHT_CHANGE = False
                LEFT_CHANGE = False
                #disable enter temporarily
                return_disabled = True
                # if player hits space, move to next dialogue and clear key input
                if key == pygame.K_SPACE:
                    dialogue_i += 1
                    key = None
                # show current label and hide previous label; if out of range of labels, mark as False
                if dialogue_i < len(node_dialogue):
                    node_dialogue[dialogue_i].show_wrap()
                else:
                    node_text = False
                    return_disabled = False
                    dialogue_i = 0

            # ENTRY TO NETWORK DIALOGUE
            if entry_text == True:
                # if player hits space, move to next dialogue and clear key input
                if key == pygame.K_SPACE:
                    dialogue_i += 1
                    key = None
                # show current label and hide previous label; if out of range of labels, start game
                if dialogue_i < len(entry_dialogue):
                    entry_dialogue[dialogue_i].show_wrap()
                else:
                    dialogue_i = 0
                    entry_text = False

            # change screens on node-enter-press
            if gamescreen == 0:
                if key == pygame.K_RETURN and return_disabled == False:
                    coords = [player_row, player_column]
                    poi = find_poi(coords, active_grid)
                    if poi == 1:
                        newgrid = True
                        gamescreen = 1
                    if poi == 2:
                        newgrid = True
                        gamescreen = 2
                    if poi == 3:
                        newgrid = True
                        gamescreen = 3
                    if poi == 4:
                        newgrid = True
                        gamescreen = 4
                    if poi == 5:
                        newgrid = True
                        gamescreen = 5
                    if poi == 6:
                        newgrid = True
                        gamescreen = 6
                if len(mazes_visited) == 6:
                    newgrid = True
                    gamescreen = 7
            # go back to network map if player hits backspace or goes to end of maze
            elif gamescreen != 0 and gamescreen != 7:
                if key == pygame.K_BACKSPACE:
                    gamescreen = 0
                    newgrid = True

            # render version text
            txt = font2.render("MAZES_V0.4_started_apr_19", True, "White")
            screen.blit(txt, (10, 680))

            # add in soundtrack buttons
            screen.blit(playpause, (670,673))
            screen.blit(vol_up, (630,670))
            screen.blit(vol_down, (600,670))
            # if playing and audio ends, loop
            if pygame.mixer.get_busy() == False and playing == True:
                soundtrack.play()

            pygame.display.flip()

            dt = clock.tick(30) / 1000
            await asyncio.sleep(0)

        while end_screen:
            # basic event utilities
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start_screen = False
                    maze_screen = False
                    running = False
                    end_screen = False
                if event.type == pygame.KEYUP:
                    key = event.key
                if event.type == pygame.MOUSEBUTTONDOWN:
                    handle_soundtrack(pygame.mouse.get_pos(), soundtrack2)
                if event.type == pygame.MOUSEWHEEL:
                    if event.y == -1:
                        mouse_dir = 'DOWN'
                    elif event.y == 1:
                        mouse_dir = 'UP'
                    else:
                        mouse_dir = None

            # make screen black
            screen.fill("Black")

            # end dialogue shit
            if end_dialogue_active == True:
                if end_once == True:
                    end_dialogue = end_dialogues()
                    end_once = False
                # if player hits space, move to next dialogue and clear key input
                if key == pygame.K_SPACE:
                    dialogue_i += 1
                    key = None
                # show current label and hide previous label; if out of range of labels, mark as False
                if dialogue_i < len(end_dialogue):
                    if dialogue_i == 8:
                        end_dialogue[dialogue_i].show_scroll_italic(mouse_dir)
                    elif dialogue_i == 9:
                        end_dialogue[dialogue_i].show_scroll_italic(mouse_dir)
                    elif dialogue_i == 14:
                        end_dialogue[dialogue_i].show_scroll_italic(mouse_dir)
                    elif dialogue_i == 15:
                        end_dialogue[dialogue_i].show_scroll_italic(mouse_dir)
                    elif dialogue_i == 16:
                        end_dialogue[dialogue_i].show_scroll_italic(mouse_dir)
                    elif dialogue_i == 17:
                        end_dialogue[dialogue_i].show_scroll_italic(mouse_dir)
                    elif dialogue_i == 18:
                        end_dialogue[dialogue_i].show_scroll_italic(mouse_dir)
                    elif dialogue_i == 19:
                        end_dialogue[dialogue_i].show_scroll_italic(mouse_dir)
                    elif dialogue_i == 20:
                        end_dialogue[dialogue_i].show_scroll_italic(mouse_dir)
                    elif dialogue_i == 21:
                        end_dialogue[dialogue_i].show_scroll_italic(mouse_dir)
                    elif dialogue_i == 22:
                        end_dialogue[dialogue_i].show_scroll_italic(mouse_dir)
                    else:
                        end_dialogue[dialogue_i].show_scroll(mouse_dir, evt)
                    mouse_dir = None
                else:
                    end_dialogue_active = False
                    goodbye_dialogue_active = True
                    dialogue_i = 0

            # end dialogue shit
            if goodbye_dialogue_active == True:
                screen.fill(WALL_COLOR)
                if goodbye_once == True:
                    goodbye_dialogue = player_goodbye()
                    goodbye_once = False
                # if player hits space, move to next dialogue and clear key input
                if key == pygame.K_SPACE:
                    dialogue_i += 1
                    key = None
                # show current label and hide previous label; if out of range of labels, mark as False
                if dialogue_i < len(goodbye_dialogue):
                    if dialogue_i >= 16:
                        goodbye_dialogue[dialogue_i].show_wrap_italic()
                    else:
                        goodbye_dialogue[dialogue_i].show_wrap()
                else:
                    end_screen = False
                    running = False
                    start_screen = False
                    maze_screen = False

            # render version text
            txt = font2.render("MAZES_V0.4_started_apr_19", True, "White")
            screen.blit(txt, (10, 680))

            # add in soundtrack buttons
            screen.blit(playpause, (670,673))
            screen.blit(vol_up, (630,670))
            screen.blit(vol_down, (600,670))
            # if playing and audio ends, loop
            if pygame.mixer.get_busy() == False and playing == True:
                soundtrack2.play()

            pygame.display.flip()

            dt = clock.tick(30) / 1000
            await asyncio.sleep(0)


        while start_screen:
            # basic event utilities
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start_screen = False
                    maze_screen = False
                    running = False
                if event.type == pygame.KEYUP:
                    key = event.key
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        handle_soundtrack(pygame.mouse.get_pos(), soundtrack)
                    if event.button == 5:
                        mouse_dir = "DOWN"
                    elif event.button == 4:
                        mouse_dir = "UP"

            screen.fill(WALL_COLOR)

            # if player hits space, move to next label and clear key input
            if key == pygame.K_SPACE:
                dialogue_i += 1
                key = None

            # show current label and hide previous label; if out of range of labels, start game
            if dialogue_i < len(labels):
                labels[dialogue_i].show_wrap()
            else:
                # be sure to set dialogue_i back to zero!
                dialogue_i = 0
                start_screen = False
                maze_screen = True

            # render version text
            txt = font2.render("MAZES_V0.4_started_apr_19", True, "White")
            screen.blit(txt, (10, 680))

            # add in soundtrack buttons
            screen.blit(playpause, (670,673))
            screen.blit(vol_up, (630,670))
            screen.blit(vol_down, (600,670))
            # if playing and audio ends, loop
            if pygame.mixer.get_busy() == False and playing == True:
                soundtrack.play()

            pygame.display.flip()

            dt = clock.tick(30) / 1000
            await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
