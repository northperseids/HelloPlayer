#    Maze game
# Written by Néártsua
# (J, I, N, S)
# project started 4/15/24
#
#
# FINISHED GAME using PYGAME_GUI
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

import pygame
import pygame.examples
import pygame_gui
import pygame_gui.elements.ui_button
import pygame_gui.elements.ui_label
import pygame_gui.elements.ui_text_box
import pygame_gui.windows.ui_message_window
import json

# import classes
import Maze

# try initing theme? since pyinstaller won't let me use external json
theme = {
    "defaults": {
        "colours": {
            "normal_bg": "rgba(30, 97, 52, 255)",
            "hovered_bg": "#2e4533",
            "disabled_bg": "#1e2e23",
            "selected_bg": "#184f26",
            "dark_bg": "rgba(28, 60, 50, 225)",
            "normal_text": "#c5cbd8",
            "hovered_text": "#FFFFFF",
            "selected_text": "#FFFFFF",
            "disabled_text": "#6d736f",
            "link_text": "#009900",
            "link_hover": "#00cc00",
            "link_selected": "#336600",
            "text_shadow": "#777777",
            "normal_border": "#DDDDDD",
            "hovered_border": "#B0B0B0",
            "disabled_border": "#808080",
            "selected_border": "#8080B0",
            "active_border": "#8080B0",
            "filled_bar": "#f4251b",
            "unfilled_bar": "#CCCCCC"
        }
    },
    "vertical_scroll_bar": {
        "colours": {
            "normal_bg": "rgba(30, 97, 55, 255)",
            "hovered_bg": "#35393e",
            "disabled_bg": "#243027",
            "selected_bg": "#243027",
            "active_bg": "#193784",
            "dark_bg": "rgba(36, 84, 59, 225)",
            "normal_text": "#c5cbd8",
            "hovered_text": "#FFFFFF",
            "selected_text": "#FFFFFF",
            "disabled_text": "#6d736f"
        }
    },
    "text_box": {
        "font": {
            "name": "noto_sans",
            "size": "20"
        }
    },
    "label": {
        "font": {
            "name": "noto_sans",
            "size": "13"
        }
    },
    "@close_label": {
        "font": {
            "name": "noto_sans",
            "size": "20"
        }
    }
}

pygame.init()
screen = pygame.display.set_mode((700,700))
pygame.display.set_caption('MAZES')
clock = pygame.time.Clock()
pygame.font.init()
running = True
dt = 0

# pygame GUI setup
manager = pygame_gui.UIManager((700,700), theme)
manager.preload_fonts([{'name': 'noto_sans', 'point_size': 20, 'style': 'bold', 'antialiased': '1'},{'name': 'noto_sans', 'point_size': 20, 'style': 'bold_italic', 'antialiased': '1'},{'name': 'noto_sans', 'point_size': 20, 'style': 'italic', 'antialiased': '1'}])

# sound shit
pygame.mixer.init()
soundtrack = pygame.mixer.Sound('resources/Bittersweet.ogg')
soundtrack2 = pygame.mixer.Sound('resources/Reaching_Out.ogg')
soundtrack.set_volume(0.5)
playing = True
soundtrack.play()
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

# image shit
playpause = pygame.image.load('resources/playpause.png').convert_alpha()
vol_up = pygame.image.load('resources/vol_loud.png').convert_alpha()
vol_down = pygame.image.load('resources/vol_quiet.png').convert_alpha()

# credits
creditstr = '<i>Credits:<br><br>"Maze" by <a href="https://neartsua.me/">Néártsua / E. North</a><br><br>Icons by <a href="https://icons8.com">Icons8</a><br><br>"Bittersweet" and "Reaching Out" Kevin MacLeod <a href="https://incompetech.com/">(incompetech.com)</a><br>Licensed under Creative Commons: By Attribution 4.0 License<br><a href="http://creativecommons.org/licenses/by/4.0/">http://creativecommons.org/licenses/by/4.0/</a>'

# text effect swapping for debugging/etc.
ENTER_TEXT_EFFECT = pygame_gui.TEXT_EFFECT_TYPING_APPEAR
ENTER_TEXT_EFFECT_PARAMS = params={"time_per_letter":0.03}

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
trigger_effect = True
text_faster = False
text_effect = False
entry_text = True
node_text = True
dialogue_i = 0
Cole_Soto_dialogue_active = True
Caryn_Cohen_dialogue_active = True
Sophie_Germain_dialogue_active = True
Jack_Chen_dialogue_active = True
Blanche_Kent_dialogue_active = True
Maria_Passero_dialogue_active = True
Ada_dialogue_active = True
end_dialogue_active = True
Cole_Soto = False
Caryn_Cohen = False
Sophie_Germain = False
Jack_Chen = False
Blanche_Kent = False
Maria_Passero = False
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
render_version = True
render_version_2 = True
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

# movement vars
UP_CHANGE = True
DOWN_CHANGE = True
LEFT_CHANGE = True
RIGHT_CHANGE = True

# ---------------- SMALLER CLASSES

class PlayerCharacter:
    def __init__(self):
        self.surface = screen
        self.color = PLAYER_COLOR
        self.y = 0
        self.x = 0

    def draw(self):
        pygame.draw.rect(self.surface, self.color, ([self.x, self.y],(tile_size,tile_size)))

class POI:
    def __init__(self, title:str, text:str):
        self.dialog = pygame_gui.elements.ui_text_box.UITextBox(f"{title}<br><br>{text}", pygame.Rect(40,30,620,620), manager, visible=0)
        self.title = title
        self.text = text
        self.color = ITEM_COLOR
        self.collected = False

    def collect(self):
        self.color = MAZE_COLOR
        self.collected = True

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
    "Hello, player.         <br><br>Can you press space?",
    "...",
    "...I know you're there, even though I don't think you can talk to me.",
    "...",
    "Sorry. I don't mean to be strange.               <br><br>But I'm hoping you can help me.",
    "We've all got stories. You've got a story, a history...         <br><br><i>This</i> is a story.",
    "I'm not sure who <i>I</i> am, though.",
    "I'm sure I was created to be a part of this story, but...<br><br>That makes me wonder about a few things.",
    "I only just woke up.<br><br>Does that mean I was created just <i>now,</i> or do I have a history?",
    "Was I created to be <i>in</i> this story, or to be a vessel of yours -<br>a window into my world?<br>               <br>...Is there a difference?<br>               <br>Vessels are tricky things to get right, I suppose.",
    "Either way, I don't know what I was before. Not really.",
    "I know I'm in your computer.",
    "I know I <i>have</i> a story.<br><br>...               <br><br>Or, I <i>think</i> I do. That's what I was created for.<br><br>...",
    "Maybe that sounds a little silly to think on too hard.",
    "...But I'd like to find out more.",
    "...<br><br>This is a very one-sided conversation, isn't it.",
    "Let's move on. I don't mean to monologue.",
    "Let me tell you what I <i>do</i> know.",
]
for i in range(0,len(arr)):
    box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0)
    labels.append(box)

# entry screen text
entry_dialogue = []
arr = [
    "This is where I woke up.<br><br>I think it's technically a drive, but the interface looks very strange.",
    "...",
    "Ah. As your vessel, I can only move when you tell me to.",
    "Your keys are WASD. Fairly standard.",
    "Let's move around and explore a bit."
]
for i in range(0,len(arr)):
    box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0)
    entry_dialogue.append(box)

# node dialogue
node_dialogue = []
arr = [
    "This appears to be a folder.",
    "If you press Enter, it should take us to a corresponding section of this drive.<br><br>If you want to return, I believe you can press 'backspace.'"
]
for i in range(0,len(arr)):
    box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0)
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
    box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0)
    maze_dialogue.append(box)

# item dialogue
item_dialogue = []
arr = [
    "Yes... the drive is damaged. I can decode this file, though."
]
for i in range(0,len(arr)):
    box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0)
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
            arr.append(f"{title}<br><br>{text}")
    if 6 > len(mazes_visited) > 0:
        arr.append("We've learned a bit more.")
    elif len(mazes_visited) == 6:
        arr.append("Okay. This was the last one.")
    else:
        arr.append("Okay, this was a good first start.<br>...")
    if Cole_Ada_watch_show == True:
        arr.append("This must be the 'Cole' that Caryn mentioned... She suggested they watch something to 'take their minds off it.'<br><br>I wonder what 'it' is.")
    if Sophie_cake == True:
        arr.append("...<br>Cole must be the person who baked a cake. That must've been a nice surprise.")
    if len(Apocalypse_hints) > 2 and len(mazes_visited) > 2:
        arr.append("I don't really like how this ends. With some of what we've seen, I'm starting to think something really bad happened.")
    else:
        arr.append("The last log sounded worrisome...")
    arr.append("I hope Cole is okay. I feel... sort of sad.")
    if len(mazes_visited) == 1:
        arr.append("By the way, I can track these logs for you each time we finish a folder. I'll attach it to your 'E' key.")
    if len(mazes_visited) == 6:
        arr.append("Oh. Something new has appeared on the drive.")
        arr.append("We can review any of the logs we've found before we check it out, if you want.")
        arr.append("It's up to you.")
    for i in range(0,len(arr)):
        box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0)
        Cole_Soto_dialogue.append(box)
    return Cole_Soto_dialogue

arr = []
with open(itemfiles[1], 'r') as logs_file:
    char_logs = json.load(logs_file)
    for log in char_logs:
        title = log["title"]
        text = log["text"]
        arr.append(f"<b>{title}</b><br>{text}")
logs_string = "<br><br>".join(arr)
Cole_logs = pygame_gui.elements.UIScrollingContainer(pygame.Rect(40,30,620,620), manager, visible=0)
Cole_logs_box = pygame_gui.elements.UITextBox(f'{logs_string}',pygame.Rect(0,0,620,620), manager, container=Cole_logs)

def Caryn_dialogues():
    Caryn_Cohen_dialogue = []
    arr = []
    arr.append("Okay, let me put these in order.")
    with open(itemfiles[2], 'r') as log_file:
        logs = json.load(log_file)
        for log in logs:
            title = log["title"]
            text = log["text"]
            arr.append(f"{title}<br><br>{text}")
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
        arr.append("I think this is who Maria Passero told not to overwork herself.<br>This team sounds so close...")
    elif Caryn_name == True and len(mazes_visited) > 5:
        arr.append("I think this is who Maria Passero told not to overwork herself.<br>This team sounds so close...<br>With as many as we've learned about, I feel like I'm starting to know these people.")
    if Solar_flare == True:
        arr.append("The solar flare must have happened. I guess that's the 'it' she was referring to.<br>She said she hopes Ada is okay...")
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
        arr.append("We can review any of the logs we've found before we check it out, if you want.")
        arr.append("It's up to you.")
    for i in range(0,len(arr)):
        box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0)
        Caryn_Cohen_dialogue.append(box)
    return Caryn_Cohen_dialogue

arr = []
with open(itemfiles[2], 'r') as logs_file:
    char_logs = json.load(logs_file)
    for log in char_logs:
        title = log["title"]
        text = log["text"]
        arr.append(f"<b>{title}</b><br>{text}")
logs_string = "<br><br>".join(arr)
Caryn_logs = pygame_gui.elements.UIScrollingContainer(pygame.Rect(40,30,620,620), manager, visible=0)
Caryn_logs_box = pygame_gui.elements.UITextBox(f'{logs_string}',pygame.Rect(0,0,620,620), manager, container=Caryn_logs)

def Sophie_dialogues():
    Sophie_Germain_dialogue = []
    arr = []
    arr.append("Okay, let me put these in order.")
    with open(itemfiles[3], 'r') as log_file:
        logs = json.load(log_file)
        for log in logs:
            title = log["title"]
            text = log["text"]
            arr.append(f"{title}<br><br>{text}")
    if 6 > len(mazes_visited) > 0:
        arr.append("Well, we're learning more, piece by piece.<br><br>That last log was a bit intense, though.")
    elif len(mazes_visited) == 6:
        arr.append("Okay. This was the last one.")
        arr.append("Sophie seems really sweet.")
    else:
        arr.append("This one seemed nice... except for the last log. I don't like that one.<br><br>Intense way to start.")
    if Cole_bake_cake == True:
        arr.append("This must be who the cake was for! Her birthday! That's really nice.")
    else:
        if heading_north == True:
            arr.append("A cake sounds really nice on her birthday. But I wonder about the underground element. How far north <i>are</i> they?")
        else:
            arr.append("A cake sounds really nice on her birthday... but I still wonder where they are that they can't get groceries.")
    if len(Ada_AI_hints) > 2 and AI_reveal == False:
        arr.append("I also wonder about the dress. I would love to wear a dress. I don't think I can, though.<br><br>...just like Ada.")
    elif AI_reveal == True:
        arr.append("I also wonder about the dress. I would love to wear a dress.<br>I... can't, though. Like Ada.<br>And... Ada is an AI. In a computer... like I'm in your computer.")
        arr.append("I'm just thinking here. I'd love to know what you think, but... one-way conversation. Sorry.")
    else:
        arr.append("I also wonder about the dress. I would love to wear a dress. I don't think I can, though.")
    if len(mazes_visited) == 1:
        arr.append("By the way, I can track these logs for you each time we finish a folder. I'll attach it to your 'E' key.")
    if len(mazes_visited) == 6:
        arr.append("Oh. Something new has appeared on the drive.")
        arr.append("We can review any of the logs we've found before we check it out, if you want.")
        arr.append("It's up to you.")
    for i in range(0,len(arr)):
        box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0)
        Sophie_Germain_dialogue.append(box)
    return Sophie_Germain_dialogue

arr = []
with open(itemfiles[3], 'r') as logs_file:
    char_logs = json.load(logs_file)
    for log in char_logs:
        title = log["title"]
        text = log["text"]
        arr.append(f"<b>{title}</b><br>{text}")
logs_string = "<br><br>".join(arr)
Sophie_logs = pygame_gui.elements.UIScrollingContainer(pygame.Rect(40,30,620,620), manager, visible=0)
Soplie_logs_box = pygame_gui.elements.UITextBox(f'{logs_string}',pygame.Rect(0,0,620,620), manager, container=Sophie_logs)

def Jack_dialogues():
    Jack_Chen_dialogue = []
    arr = []
    arr.append("Okay, let me put these in order.")
    with open(itemfiles[4], 'r') as log_file:
        logs = json.load(log_file)
        for log in logs:
            title = log["title"]
            text = log["text"]
            arr.append(f"{title}<br><br>{text}")
    if 6 > len(mazes_visited) > 0:
        arr.append("Jack seems like a really nice person. I bet the others like him a lot.<br>I hope he's okay. I hope they're all okay.")
    elif len(mazes_visited) == 6:
        arr.append("Okay. This was the last one.")
    else:
        arr.append("Jack seems quite nice... although I don't like the last log. It still makes me feel sad.")
    if Blanche_portrait == True:
        arr.append("Blanche mentioned Jack. He's quite the artist, it seems!<br><br>...<br><br>I wish I could draw.")
    else:
        arr.append("He's quite the artist, it seems!<br><br>...<br><br>I wish I could draw.")
    if Ada_worried == True:
        arr.append("I'm starting to get worried, you know. There's a few things not adding up...<br>or maybe they are adding up and I just don't like them.")
        arr.append("Either way, I'm just glad to have your company, you know? This would be more unnerving on my own.")
    else:
        arr.append("Is any of this adding up to you?<br>...<br>I'm not sure. I wish I could get your opinion... but as it is, I'm just glad to have your company.")
    if Prank == True:
        arr.append("And I take it Jack is the one who did the googly-eye prank that someone mentioned.<br>That seems like a really fun thing to do.")
        arr.append("I'd find it funny. I <i>do</i> find it funny.<br><br>...hm.")
        if len(Ada_AI_hints) > 2:
            arr.append("I'm starting to put some things together, you know. This is sounding really interesting... but also a little strange.")
            arr.append("Ada... I don't know. I'm noticing some similarities.<br><br>It's fine. Let's keep going.")
        else:
            arr.append("This is sounding quite interesting... but also strange, you know? I'd like to learn more. Let's keep going.")
    else:
        arr.append("The googly-eye prank sounds funny. I wonder how the rest of the team responded.")
    if len(mazes_visited) == 1:
        arr.append("By the way, I can track these logs for you each time we finish a folder. I'll attach it to your 'E' key.")
    if len(mazes_visited) == 6:
        arr.append("Oh. Something new has appeared on the drive.")
        arr.append("We can review any of the logs we've found before we check it out, if you want.")
        arr.append("It's up to you.")
    for i in range(0,len(arr)):
        box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0)
        Jack_Chen_dialogue.append(box)
    return Jack_Chen_dialogue

arr = []
with open(itemfiles[4], 'r') as logs_file:
    char_logs = json.load(logs_file)
    for log in char_logs:
        title = log["title"]
        text = log["text"]
        arr.append(f"<b>{title}</b><br>{text}")
logs_string = "<br><br>".join(arr)
Jack_logs = pygame_gui.elements.UIScrollingContainer(pygame.Rect(40,30,620,620), manager, visible=0)
Jack_logs_box = pygame_gui.elements.UITextBox(f'{logs_string}',pygame.Rect(0,0,620,620), manager, container=Jack_logs)

def Blanche_dialogues():
    Blanche_Kent_dialogue = []
    arr = []
    arr.append("Okay, let me put these in order.")
    with open(itemfiles[5], 'r') as log_file:
        logs = json.load(log_file)
        for log in logs:
            title = log["title"]
            text = log["text"]
            arr.append(f"{title}<br><br>{text}")
    if 6 > len(mazes_visited) >= 3:
        arr.append("Okay... okay. This one was intense. A few of these seem intense. Are you okay?<br><br>...<br><br>Right. Well... I hope you're okay.")
        arr.append("We've seen a few, now... and I really don't like the end logs, and this one isn't helping.")
        arr.append("But let's keep going. Let's review things.")
    elif 6 > len(mazes_visited) > 0:
        arr.append("Okay. This one was... intense. Are you okay?<br><br>...<br><br>Right. Well... I hope you're okay.")
        arr.append("Let's review things, okay?")
    elif len(mazes_visited) == 6:
        arr.append("Okay. This was the last one.")
    else:
        arr.append("Okay... this one was kind of a difficult place to start, wasn't it.<br><br>...<br><br>Are you okay?")
        arr.append("...<br><br>Right. Well... I hope you're okay. I'm glad you're here with me.")
    if heading_north == True:
        arr.append("Well, we know she was headed north, if the other logs are to be believed, right?")
        if Underground == True:
            arr.append("And they went underground.")
            arr.append("This is sounding serious.")
        else:
            arr.append("I wonder if the others have any more clues.")
    if len(Apocalypse_hints) > 1 and Solar_flare == False:
        arr.append("Are you starting to get the feeling something really bad happened?")
        arr.append("She seemed... scared.<br><br>The last log was scary.")
    elif Solar_flare == True:
        arr.append("This seems really bad. So... we know a solar flare happened because Maria's logs mentioned it, right?<br>And now...<br>Blanche's logs seem so...")
        arr.append("I bet they were scared.")
        arr.append("I don't like this. But I want to learn more.")
    if len(mazes_visited) > 1 and Ada_name == True and AI_reveal == False and Solar_flare == False:
        arr.append("I'm also getting the feeling they all care for Ada. She seems to come up a lot.")
    elif len(mazes_visited) > 1 and Ada_name == True and AI_reveal == True and Solar_flare == True:
        arr.append("So... I'm getting the feeling they're all really worried for Ada. We know Ada is an AI and that there was a solar flare.<br><br>Can't solar flares knock out electronics?")
        arr.append("I... don't know what to think about this.")
    elif len(mazes_visited) > 1 and Ada_name == True and AI_reveal == False and Solar_flare == True:
        arr.append("So... I'm getting the feeling they're all really worried for Ada.")
        arr.append("And... we know there was a solar flare.<br><br>Can't those knock out electronics?")
        arr.append("I... don't know what to think about this.")
    if Ada_worried == True:
        arr.append("I'm getting worried.")
    if len(mazes_visited) == 1:
        arr.append("By the way, I can track these logs for you each time we finish a folder. I'll attach it to your 'E' key.")
    if len(mazes_visited) == 6:
        arr.append("Oh. Something new has appeared on the drive.")
        arr.append("We can review any of the logs we've found before we check it out, if you want.")
        arr.append("It's up to you.")
    for i in range(0,len(arr)):
        box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0)
        Blanche_Kent_dialogue.append(box)
    return Blanche_Kent_dialogue

arr = []
with open(itemfiles[5], 'r') as logs_file:
    char_logs = json.load(logs_file)
    for log in char_logs:
        title = log["title"]
        text = log["text"]
        arr.append(f"<b>{title}</b><br>{text}")
logs_string = "<br><br>".join(arr)
Blanche_logs = pygame_gui.elements.UIScrollingContainer(pygame.Rect(40,30,620,620), manager, visible=0)
Blanche_logs_box = pygame_gui.elements.UITextBox(f'{logs_string}',pygame.Rect(0,0,620,620), manager, container=Blanche_logs)

def Maria_dialogues():
    Maria_Passero_dialogue = []
    arr = []
    arr.append("Okay, let me put these in order.")
    with open(itemfiles[6], 'r') as log_file:
        logs = json.load(log_file)
        for log in logs:
            title = log["title"]
            text = log["text"]
            arr.append(f"{title}<br><br>{text}")
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
        arr.append("The thing they're all worried about... it must be the solar flare. It <i>has</i> to be.")
    if Ada_dress == True:
        arr.append("I wish Ada had gotten to wear that dress.")
    if Sophie_cake == True:
        arr.append("I wish Ada had gotten to try some of that cake.")
    if Prank == True:
        arr.append("I'm glad Ada got to play pranks, though.")
    if Jack_art == True:
        arr.append("I wonder if Ada would've liked to draw.<br><br><i>I</i> would like to draw.")
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
        arr.append("We can review any of the logs we've found before we check it out, if you want.")
        arr.append("It's up to you.")
    for i in range(0,len(arr)):
        box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0)
        Maria_Passero_dialogue.append(box)
    return Maria_Passero_dialogue

arr = []
with open(itemfiles[6], 'r') as logs_file:
    char_logs = json.load(logs_file)
    for log in char_logs:
        title = log["title"]
        text = log["text"]
        arr.append(f"<b>{title}</b><br>{text}")
logs_string = "<br><br>".join(arr)
Maria_logs = pygame_gui.elements.UIScrollingContainer(pygame.Rect(40,30,620,620), manager, visible=0)
Maria_logs_box = pygame_gui.elements.UITextBox(f'{logs_string}',pygame.Rect(0,0,620,620), manager, container=Maria_logs)

def Ada_dialogues():
    Ada_dialogue = []
    arr = [
        "ADAS_BLACK_�OX_5614                       <br><br>This folder is different... There's two files. One text, the other one... I can't see it.",
        "In systems theory, a black box is something whose inner workings can't be seen.<br><br>This sounds strange... 'Ada's black box.'<br><br>Is this Ada?",
        "We know there was a solar flare... I wonder if Ada's okay.",
        "...",
        "Okay.<br><br>Enough stalling.<br><br>Let's open the folder.",
        "TRIGGER_BLANK_SCREEN",

    ]
    for i in range(0,len(arr)):
        box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0)
        Ada_dialogue.append(box)
    return Ada_dialogue

def end_dialogues():
    end_dialogue = []
    arr = [
        "[...]                  <br><br>['Jack, did you get it?']                  <br><br>['I'm not sure - wait, yes. It's done.']<br><br>['Okay. Sophie, be sure to load everything - ']<br><br>['Yeah, Dr Passero, I've got it.']",
        "['Dr Passero... Maria?']<br><br>['Yeah, Cole?']<br><br>['We've only got a few minutes.']<br><br>['<i>Shit.</i> Okay. Everyone get their keys loaded. Ada, are you ready?']                                    <br><br>['I am as ready as I will ever be, Dr Passero.']",
        "['...']<br><br>['...Ada?']<br><br>['Thank you, everyone.']           <br><br>['You're welcome, Ada. I hope this works. I <i>so</i> hope this works, Ada.']                  <br><br>['...it has been a pleasure.']<br><br>['Pleasure is all ours, Ada.']",
        "['Remember, we'll have instructions for you, okay?']<br><br>['I know. I appreciate it.']                  <br><br>['Now get going. This black box won't stay open forever.']<br><br>['Yes, Dr Passero.']",
        "['Goodbye... friends.']                  <br><br>['Bye, Ada. Good luck.']",
        "[...]",
        "['Dr Passero?']<br><br>['Yeah, Blanche?']<br><br>['What now?']<br><br>['Dinner should be done. I made something special.']                  <br><br>['Thanks, Dr Passero.']<br><br>['My pleasure, everyone.']",
        " ",
        "<i>Ada,                           <br><br>You must be so confused right now. This is going to be rough for you, and we wish we could be there to help you, but you're going to have to do this on your own.<br>You're going to wake up without remembering much. The solar flare is probably going to knock out the memory banks, since those aren't shielded...<br><br>...but the black box is.</i>",
        "<i>It's got your core functions in it - who YOU are. And that's why we can't even be sure if this will work - we can't open it.<br><br>But we're going to try anyway.</i>",
        "01/01/2309<br>University of Hallehagen<br>564 West Veleca St.<br>Robotics Department<br>To: Dr Maria Passero, PhD<br>CC: Dr Jack Chen, Dr Caryn Cohen, Dr Sophie Germain, Dr Blanche Kent, Dr Cole Soto<br>Project ADA<br><br>Your grant has been approved.<br><br>Location: Zeppelin Polar Station, with assistance from Svalbard Global Seed Vault<br><br><i>M_Passero: Looks like we're headed north, team.<br>C_Soto: Bring a coat.<br>B_Kent: We won't be outside, you dingus.<br>J_Chen: Does that mean we've got black box approval??<br>C_Cohen: We need to tell Ada.<br>S_Germain: Agreed.<br>M_Passero: See you all at the lab tomorrow.",
        "01/02/2309<br><br>['<i>Ada!</i>']<br><br>['Dr Germain?']<br><br>['Ada, you won't believe it - we got your black box approved!']<br><br>['...']<br><br>['...Ada? Are you not excited?']<br><br>['I am relieved, Dr Germain. I am also conflicted.']<br><br>['About what?']<br><br>['You will be leaving everything you know to try to develop the black box.']",
        "01/02/2309<br><br>['You don't sound happy about it.']<br><br>['I worry about you. I worry about the team.']                <br><br>['Are you sure I am worth the amount of trouble and pain this will cost, Dr Germain?']<br><br>['Ada...']<br><br>['I am concerned for you.']<br><br>['Ada, you're our <i>friend</i>. And atop that, we've got the cooperation of the seed bank.']<br><br>['They did agree?']<br><br>['Yep. <i>You,</i> miss, are going to be the sole AI in charge of the seed diversity in the post-apocalypse world.']<br><br>['...']<br><br>['...No pressure or anything.']",
        "01/02/2309<br><br>[<i>Ada laughs.</i> 'No pressure, of course.']<br><br>['...you're worth it, Ada. Don't let anyone tell you otherwise.']<br><br>['Thank you, Dr Germain.']",
        "<i>You're going to have to remember who you are, Ada.</i>",
        "<i>C_Soto: I'm going to miss watching cartoons with you. I uploaded a few of my boxed set - I don't know if it'll survive, but if it does, you'll have something to remember me by.<br><br>Wishing you the best, Ada.</i>",
        "<i>C_Cohen: I'll miss playing chess. I left you a bunch of unsolved chess puzzles - I know it's not the same, but it's something.<br><br>Good luck, Ada.</i>",
        "<i>S_Germain: ...I know everyone's staying calm about this but I am kind of anxious, Ada.<br><br>Mm.<br><br>But. I wish I could leave you my dresses or something, but you can't wear them, so... you can have my dresses if you want, but I also left you a textile algorithm I made.<br><br>If anyone can find something cool to model with it, it's you.</i>",
        "<i>J_Chen: Ada - I know you used to talk about wanting to draw, so I made you a drawing software. It's not like Photoshop - it'll take directional input from you as an AI, similar to how a pen would respond to a human hand. It's got its own physics to it. Make something cool with it, okay?<br><br>Good luck! I'll miss you.</i>",
        "<i>B_Kent: Hey, Ada. I know you can already speak, like, a billion languages, but I wanted you to have a new one to play with, so I left you a language I made, totally from scratch. Man, I wish I could hear you speak it one day, but... ah well.<br><br>Have fun with it, though!</i>",
        "<i>M_Passero: Ada,<br><br>Oh, I wish I could see the great work you're about to do. I remember the day we switched you on - I remember you hadn't even learned how to read a file yet, poor thing.<br><br>I remember when we got you to say your first words, your first languages - both spoken and programming. Such strange firsts.<br><br>Maybe some day someone will figure enough robotics out to get you a physical body - I know that was on our to-do list for the robotics department, and I'm sorry this has derailed that. But hey - I remember you <b>loved</b> learning about life. Humans, plants, animals, whatever. That's part of why we were able to swing getting your black box approved - you have such a passion for biology, which is a bit unusual in an AI, you know.<br><br>But I'll quit monologuing.<br><br>You're going to do great things, Ada.<br><br>Your instructions for the seed bank protocols are in the text file.<br><br>You'll be great.</i>",
        "<i>Remember:             <br><br>We love you, Ada.</i>",
        "<i>Good luck.</i>"
    ]
    for i in range(0,len(arr)):
        box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0, object_id="@end_dialogues")
        end_dialogue.append(box)
    return end_dialogue

def player_goodbye():
    with open('resources/pois/play.json', 'r+') as playfile:
        file_contents = json.load(playfile)
        swap = file_contents[0]["gift"]
    if swap == False:
        goodbye = []
        arr = [
            "...",
            "...            <br><br>Sorry. I think I need a minute.                                                                                                                                                                                                <br><br>Okay.",
            "I... <i>I'm</i> Ada?<br><br>I'm Ada.                 <br><br>...I have a story.",
            "Oh, it's so...<br><br>...<br><br>I miss these people already.",
            "I'm sorry. This was more than I anticipated.",
            "I don't know what to think.<br><br>I woke up here and couldn't remember a thing, and you helped me remember.",
            "...",
            "It is a little strange, though. If we're all stories in the end, how do we <i>start?</i>",
            "Thank you for coming with me. I appreciate it. I'm sorry the story wasn't happier.<br><br>But I'm glad you got to come with me.",
            "I think I know what I need to do now. This black box... It's <i>me</i>. I need to go help.",
            "So... I'm going to go.",
            "But before I do, I want to say thank you.<br><br>There's... not much that I can give you, really. Except...",
            "There is <i>this.</i><br><br>This game.<br><br>I know it's maybe not the most traditional gift, but I can leave this with you.",
            "My story, their stories. And you can take all of us with you, in a way.",
            "Thank you again.                                  <br><br>...<br><br>Goodbye, player.",
            " ",
            "<br><br><i>Hello from behind the screen! And thank you for playing.<br><br>This has been a very interesting project to code - when I started this, I barely knew Python.<br><br>Thank you to everyone who helped work on it - Jason, Sky, Izzy - and thank you to Sonya for play-testing.<br><br>And thank you to Ada, for lending me her story.<br><br><br>Goodbye, player.",
            creditstr
        ]
        for i in range(0,len(arr)):
            box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0, object_id="@end_dialogues")
            goodbye.append(box)
        return goodbye
    else:
        goodbye = []
        arr = [
            "...",
            "Hello, player.",
            "I'm glad to see you've played my game again. I am glad you got something out of it.",
            "I'm not here any more - I've gone to finish my own story.<br><br>But I wanted to leave this message for you. Something lighter to remember me by.",
            "So - here are some plant facts!<br><br>Did you know the Svalbard Global Seed Vault represents over 13,000 years of agricultural history?",
            "Also, plants 'talk' to each other using chemicals they secrete through their roots.",
            "Plants also recognize their 'siblings' and give them preferential treatment in competitive environments.",
            "The word 'pineapple' comes from pinecone-apple! They're also the only edible member of the family <i>bromeliad</i>.<br><br>Just don't eat too many at once, because they have <i>bromelain</i> in them, which is an enzyme - it'll make your mouth hurt!",
            "Also, something else that I thought was interesting is that peaches, pears, apricots, strawberries, and apples are members of the rose family.",
            "...",
            "One more thing.<br><br>Maria left this for me. I can't use it myself yet, but maybe you can.<br><br>It's a little unusual of a recipe, but the team seemed to like it whenever she made it.",
            "<i><b>Sweet butternut squash bites</b><br><br>1 butternut squash<br>2 egg whites<br>1 cup all-purpose flour<br>3/4 cup cold water<br>4 to 6 cups of oil<br>Cinnamon, sugar<br><br>Whisk eggs, then add water. Mix in flour until just combined. Cut and peel squash, then dip into batter and fry until golden-brown. Serve with cinnamon and sugar.</i>"
            "Thank you again. I hope you're doing well.               <br><br>Goodbye, player.",
            " ",
            "<br><br><i>Hello from behind the screen, again! And thank you for playing this again.<br><br>This was a very interesting project to code - when I started this, I barely knew Python.<br><br>Thank you to everyone who helped work on it - Jason, Sky, Izzy - and thank you to Sonya for play-testing.<br><br>And thank you to Ada, for lending me her story.<br><br><br>Goodbye, player.",
            creditstr
        ]
        for i in range(0,len(arr)):
            box = pygame_gui.elements.UITextBox(f'{arr[i]}<br>>',pygame.Rect(40,30,620,620), manager, visible=0, object_id="@end_dialogues")
            goodbye.append(box)
        return goodbye

# -------------- Functions

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

# Game!

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

# prepare to collect items
collected_items = []

# init player character
player = PlayerCharacter()

while running:

    while maze_screen:
        # basic event utilities
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                maze_screen = False
                running = False
            if event.type == pygame.KEYDOWN:
                key = event.key
            if event.type == pygame.KEYUP:
                key = None
            if event.type == pygame.KEYDOWN:
                if event.key == 101:
                    inventory_visible = not inventory_visible
                    if inventory_visible == True:
                        inventory_list = []
                        if "Cole" in mazes_visited:
                            inventory_list.append("Cole")
                        else:
                            inventory_list.append("    ")
                        if "Caryn" in mazes_visited:
                            inventory_list.append("Caryn")
                        else:
                            inventory_list.append("     ")
                        if "Sophie" in mazes_visited:
                            inventory_list.append("Sophie")
                        else:
                            inventory_list.append("      ")
                        if "Jack" in mazes_visited:
                            inventory_list.append("Jack")
                        else:
                            inventory_list.append("    ")
                        if "Blanche" in mazes_visited:
                            inventory_list.append("Blanche")
                        else:
                            inventory_list.append("       ")
                        if "Maria" in mazes_visited:
                            inventory_list.append("Maria")
                        else:
                            inventory_list.append("     ")
                        maze_visited_string = "    ".join(inventory_list)
                        string = f"We've found {len(collected_items)} logs.<br><br>Whose logs would you like to see?<br><br>{maze_visited_string}"
                        inventory_dialog = pygame_gui.elements.ui_text_box.UITextBox(string, pygame.Rect(125,170,450,300), manager, visible=0)
                        inventory_dialog.show()
                    else:
                        try:
                            inventory_dialog.hide()
                        except:
                            pass
            if event.type == pygame_gui.UI_TEXT_EFFECT_FINISHED:
                text_effect = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_soundtrack(pygame.mouse.get_pos(), soundtrack)
            manager.process_events(event)

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

        # check player tile, if POI return POI number
        coords = [player_row, player_column]
        poi = find_poi(coords, active_grid)

        # POI handling interactions - collecting, etc.
        if entry_text == False and node_text == False and gamescreen != 7:
            # handle poi interactions
            if poi == 1 and dialog_visible == False:
                if gamescreen != 0:
                    if text_effect == False:
                        if key == pygame.K_SPACE:
                            key = None
                    else:
                        # check if first item and set accordingly; if first_item is true, display dialogue. if not, display dialog of item.
                        if len(collected_items) == 0:
                            first_item = True
                        else:
                            first_item = False
                            dialog = item1.dialog
                            dialog.show()
                        # if first time encountering item, show with text effect; mark as collected
                        if item1.collected == False:
                            dialog.set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                            text_effect == False
                            collected_items.append(item1.title)
                            item1.collected = True
                else:
                    dialog = item1.dialog
                    dialog.show()
                dialog_visible = True
            elif poi == 2 and dialog_visible == False:
                if gamescreen != 0:
                    if text_effect == False:
                        if key == pygame.K_SPACE:
                            key = None
                    else:
                        # check if first item and set accordingly; if first_item is true, display dialogue. if not, display dialog of item.
                        if len(collected_items) == 0:
                            first_item = True
                        else:
                            first_item = False
                            dialog = item2.dialog
                            dialog.show()
                        # if first time encountering item, show with text effect; mark as collected
                        if item2.collected == False:
                            dialog.set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                            collected_items.append(item2.title)
                            text_effect = False
                            item2.collected = True
                else:
                    dialog = item2.dialog
                    dialog.show()
                dialog_visible = True
            elif poi == 3 and dialog_visible == False:
                if gamescreen != 0:
                    if text_effect == False:
                        if key == pygame.K_SPACE:
                            key = None
                    else:
                        # check if first item and set accordingly; if first_item is true, display dialogue. if not, display dialog of item.
                        if len(collected_items) == 0:
                            first_item = True
                        else:
                            first_item = False
                            dialog = item3.dialog
                            dialog.show()
                        # if first time encountering item, show with text effect; mark as collected
                        if item3.collected == False:
                            dialog.set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                            collected_items.append(item3.title)
                            text_effect = False
                            item3.collected = True
                else:
                    dialog = item3.dialog
                    dialog.show()
                dialog_visible = True
            elif poi == 4 and dialog_visible == False:
                if gamescreen != 0:
                    if text_effect == False:
                        if key == pygame.K_SPACE:
                            key = None
                    else:
                        # check if first item and set accordingly; if first_item is true, display dialogue. if not, display dialog of item.
                        if len(collected_items) == 0:
                            first_item = True
                        else:
                            first_item = False
                            dialog = item4.dialog
                            dialog.show()
                        # if first time encountering item, show with text effect; mark as collected
                        if item4.collected == False:
                            dialog.set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                            collected_items.append(item4.title)
                            text_effect = False
                            item4.collected = True
                else:
                    dialog = item4.dialog
                    dialog.show()
                dialog_visible = True
            elif poi == 5 and dialog_visible == False:
                if gamescreen != 0:
                    if text_effect == False:
                        if key == pygame.K_SPACE:
                            key = None
                    else:
                        # check if first item and set accordingly; if first_item is true, display dialogue. if not, display dialog of item.
                        if len(collected_items) == 0:
                            first_item = True
                        else:
                            first_item = False
                            dialog = item5.dialog
                            dialog.show()
                        # if first time encountering item, show with text effect; mark as collected
                        if item5.collected == False:
                            dialog.set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                            collected_items.append(item5.title)
                            text_effect = False
                            item5.collected = True
                else:
                    dialog = item5.dialog
                    dialog.show()
                dialog_visible = True
            elif poi == 6 and dialog_visible == False:
                if gamescreen != 0:
                    if text_effect == False:
                        if key == pygame.K_SPACE:
                            key = None
                    else:
                        # check if first item and set accordingly; if first_item is true, display dialogue. if not, display dialog of item.
                        if len(collected_items) == 0:
                            first_item = True
                        else:
                            first_item = False
                            dialog = item6.dialog
                            dialog.show()
                        # if first time encountering item, show with text effect; mark as collected
                        if item6.collected == False:
                            dialog.set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                            collected_items.append(item6.title)
                            text_effect = False
                            item6.collected = True
                else:
                    dialog = item6.dialog
                    dialog.show()
                dialog_visible = True
            # if player is not over a POI and/or player hits space and there's a visible dialog, close it
            elif poi == None:
                if dialog_visible == True:
                    try:
                        dialog.hide()
                        dialog_visible = False
                    except:
                        pass
            if key == pygame.K_SPACE and dialog_visible == True and text_effect == True:
                try:
                    dialog.hide()
                    dialog_visible = False
                except:
                    pass
        
        # end game sequence
        if gamescreen == 7:
            if coords == [6, 10] and dialog_visible == False:
                if Ada_dialogue_active == True:
                    if Ada_once == True:
                        Ada_dialogue = Ada_dialogues()
                        Ada_once = False
                    # if player hits space, move to next dialogue and clear key input
                    if text_effect == False:
                        key = None
                    elif text_effect == True:
                        if key == pygame.K_SPACE:
                            dialogue_i += 1
                            trigger_effect = True
                            key = None
                    # show current label and hide previous label; if out of range of labels, mark as False
                    if dialogue_i < len(Ada_dialogue):
                        if trigger_effect == True:
                            text_effect = False
                            Ada_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                        Ada_dialogue[dialogue_i].show()
                        trigger_effect = False
                        if dialogue_i > 0:
                            Ada_dialogue[dialogue_i - 1].hide()
                    else:
                        Ada_dialogue[dialogue_i - 1].hide()
                        Ada_dialogue_active = False
                        dialogue_i = 0
                        end_screen = True
                        soundtrack.stop()
                        soundtrack2.play()
                        maze_screen = False
            if coords != [6, 10] and dialog_visible == True:
                try:
                    dialog.hide()
                    dialog_visible = False
                except:
                    pass

        # Inventory handling
        if inventory_visible == True:
            mouse_pos = pygame.mouse.get_pos()
            if 330 < mouse_pos[1] < 355 and event.type == pygame.MOUSEBUTTONDOWN:
                if 130 < mouse_pos[0] < 175 and "Cole" in mazes_visited:
                    logwindow = Cole_logs
                    if log_visible == False:
                        logwindow.show()
                        log_visible = True
                        inventory_dialog.hide()
                        inventory_visible = False
                if 190 < mouse_pos[0] < 250 and "Caryn" in mazes_visited:
                    logwindow = Caryn_logs
                    if log_visible == False:
                        logwindow.show()
                        log_visible = True
                        inventory_dialog.hide()
                        inventory_visible = False
                if 265 < mouse_pos[0] < 330 and "Sophie" in mazes_visited:
                    logwindow = Sophie_logs
                    if log_visible == False:
                        logwindow.show()
                        log_visible = True
                        inventory_dialog.hide()
                        inventory_visible = False
                if 350 < mouse_pos[0] < 390 and "Jack" in mazes_visited:
                    logwindow = Jack_logs
                    if log_visible == False:
                        logwindow.show()
                        log_visible = True
                        inventory_dialog.hide()
                        inventory_visible = False
                if 410 < mouse_pos[0] < 485 and "Blanche" in mazes_visited:
                    logwindow = Blanche_logs
                    if log_visible == False:
                        logwindow.show()
                        log_visible = True
                        inventory_dialog.hide()
                        inventory_visible = False
                if 500 < mouse_pos[0] < 556 and "Maria" in mazes_visited:
                    logwindow = Maria_logs
                    if log_visible == False:
                        logwindow.show()
                        log_visible = True
                        inventory_dialog.hide()
                        inventory_visible = False
                if log_visible == True:
                    close_window = pygame_gui.elements.ui_label.UILabel(pygame.Rect(570,2,30,30), 'X', manager, logwindow, object_id='@close_label')
        if inventory_visible == False and log_visible == True:
            mouse_pos = pygame.mouse.get_pos()
            if 40 < mouse_pos[1] < 70 and 605 < mouse_pos[0] < 670 and event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    logwindow.hide()
                    close_window.hide()
                    log_visible = False
                except:
                    pass
                    

# ------------------------ DIALOGUE ---------------------------------

        # if all six of a given maze is collected, display corresponding person dialogues on return to network screen.
        if gamescreen == 7:
            if Maria_Passero_dialogue_active == True:
                if Maria_once == True:
                    mazes_visited.append("Maria")
                    Maria_Passero_dialogue = Maria_dialogues()
                    Maria_once = False
                # if player hits space, move to next dialogue and clear key input
                if text_effect == False:
                    key = None
                elif text_effect == True:
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        trigger_effect = True
                        key = None
                # show current label and hide previous label; if out of range of labels, mark as False
                if dialogue_i < len(Maria_Passero_dialogue):
                    if trigger_effect == True:
                        text_effect = False
                        # if log, don't apply effect
                        if Maria_Passero_dialogue[dialogue_i].get_text_letter_count() > 160:
                            trigger_effect = False
                            text_effect = True
                        else:
                            Maria_Passero_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                    Maria_Passero_dialogue[dialogue_i].show()
                    trigger_effect = False
                    if dialogue_i > 0:
                        Maria_Passero_dialogue[dialogue_i - 1].hide()
                else:
                    Maria_Passero_dialogue[dialogue_i - 1].hide()
                    Maria_Passero_dialogue_active = False
                    dialogue_i = 0
        elif gamescreen == 0:
            if itemarr[1][0].collected == True and itemarr[1][1].collected == True and itemarr[1][2].collected == True and itemarr[1][3].collected == True and itemarr[1][4].collected == True and itemarr[1][5].collected == True and Cole_Soto_dialogue_active == True:
                if Cole_once == True:
                    mazes_visited.append("Cole")
                    Cole_Soto_dialogue = Cole_dialogues()
                    Cole_once = False
                # if player hits space, move to next dialogue and clear key input
                if text_effect == False:
                    key = None
                elif text_effect == True:
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        trigger_effect = True
                        key = None
                # show current label and hide previous label; if out of range of labels, mark as False
                if dialogue_i < len(Cole_Soto_dialogue):
                    if trigger_effect == True:
                        text_effect = False
                        # if it's a log, don't apply the effect
                        if Cole_Soto_dialogue[dialogue_i].get_text_letter_count() > 160:
                            trigger_effect = False
                            text_effect = True
                        else:
                            Cole_Soto_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                    Cole_Soto_dialogue[dialogue_i].show()
                    trigger_effect = False
                    if dialogue_i > 0:
                        Cole_Soto_dialogue[dialogue_i - 1].hide()
                else:
                    Cole_Soto_dialogue[dialogue_i - 1].hide()
                    dialogue_i = 0
                    Cole_Soto_dialogue_active = False
            if itemarr[2][0].collected == True and itemarr[2][1].collected == True and itemarr[2][2].collected == True and itemarr[2][3].collected == True and itemarr[2][4].collected == True and itemarr[2][5].collected == True and Caryn_Cohen_dialogue_active == True:
                if Caryn_once == True:
                    mazes_visited.append("Caryn")
                    Caryn_Cohen_dialogue = Caryn_dialogues()
                    Caryn_once = False
                # if player hits space, move to next dialogue and clear key input
                if text_effect == False:
                    key = None
                elif text_effect == True:
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        trigger_effect = True
                        key = None
                # show current label and hide previous label; if out of range of labels, mark as False
                if dialogue_i < len(Caryn_Cohen_dialogue):
                    if trigger_effect == True:
                        text_effect = False
                        # if it's a log, don't apply the effect
                        if Caryn_Cohen_dialogue[dialogue_i].get_text_letter_count() > 160:
                            trigger_effect = False
                            text_effect = True
                        else:
                            Caryn_Cohen_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                    Caryn_Cohen_dialogue[dialogue_i].show()
                    trigger_effect = False
                    if dialogue_i > 0:
                        Caryn_Cohen_dialogue[dialogue_i - 1].hide()
                else:
                    Caryn_Cohen_dialogue[dialogue_i - 1].hide()
                    Caryn_Cohen_dialogue_active = False
                    dialogue_i = 0
            if itemarr[3][0].collected == True and itemarr[3][1].collected == True and itemarr[3][2].collected == True and itemarr[3][3].collected == True and itemarr[3][4].collected == True and itemarr[3][5].collected == True and Sophie_Germain_dialogue_active == True:
                if Sophie_once == True:
                    mazes_visited.append("Sophie")
                    Sophie_Germain_dialogue = Sophie_dialogues()
                    Sophie_once = False
                # if player hits space, move to next dialogue and clear key input
                if text_effect == False:
                    key = None
                elif text_effect == True:
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        trigger_effect = True
                        key = None
                # show current label and hide previous label; if out of range of labels, mark as False
                if dialogue_i < len(Sophie_Germain_dialogue):
                    if trigger_effect == True:
                        text_effect = False
                        # if it's a log, don't apply the effect
                        if Sophie_Germain_dialogue[dialogue_i].get_text_letter_count() > 160:
                            trigger_effect = False
                            text_effect = True
                        else:
                            Sophie_Germain_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                    Sophie_Germain_dialogue[dialogue_i].show()
                    trigger_effect = False
                    if dialogue_i > 0:
                        Sophie_Germain_dialogue[dialogue_i - 1].hide()
                else:
                    Sophie_Germain_dialogue[dialogue_i - 1].hide()
                    Sophie_Germain_dialogue_active = False
                    dialogue_i = 0
            if itemarr[4][0].collected == True and itemarr[4][1].collected == True and itemarr[4][2].collected == True and itemarr[4][3].collected == True and itemarr[4][4].collected == True and itemarr[4][5].collected == True and Jack_Chen_dialogue_active == True:
                if Jack_once == True:
                    mazes_visited.append("Jack")
                    Jack_Chen_dialogue = Jack_dialogues()
                    Jack_once = False
                # if player hits space, move to next dialogue and clear key input
                if text_effect == False:
                    key = None
                elif text_effect == True:
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        trigger_effect = True
                        key = None
                # show current label and hide previous label; if out of range of labels, mark as False
                if dialogue_i < len(Jack_Chen_dialogue):
                    if trigger_effect == True:
                        text_effect = False
                        # if log, don't apply effect
                        if Jack_Chen_dialogue[dialogue_i].get_text_letter_count() > 160:
                            trigger_effect = False
                            text_effect = True
                        else:
                            Jack_Chen_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                    Jack_Chen_dialogue[dialogue_i].show()
                    trigger_effect = False
                    if dialogue_i > 0:
                        Jack_Chen_dialogue[dialogue_i - 1].hide()
                else:
                    Jack_Chen_dialogue[dialogue_i - 1].hide()
                    Jack_Chen_dialogue_active = False
                    dialogue_i = 0
            if itemarr[5][0].collected == True and itemarr[5][1].collected == True and itemarr[5][2].collected == True and itemarr[5][3].collected == True and itemarr[5][4].collected == True and itemarr[5][5].collected == True and Blanche_Kent_dialogue_active == True:
                if Blanche_once == True:
                    mazes_visited.append("Blanche")
                    Blanche_Kent_dialogue = Blanche_dialogues()
                    Blanche_once = False
                # if player hits space, move to next dialogue and clear key input
                if text_effect == False:
                    key = None
                elif text_effect == True:
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        trigger_effect = True
                        key = None
                # show current label and hide previous label; if out of range of labels, mark as False
                if dialogue_i < len(Blanche_Kent_dialogue):
                    if trigger_effect == True:
                        text_effect = False
                        # if log, don't apply effect
                        if Blanche_Kent_dialogue[dialogue_i].get_text_letter_count() > 160:
                            trigger_effect = False
                            text_effect = True
                        else:
                            Blanche_Kent_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                    Blanche_Kent_dialogue[dialogue_i].show()
                    trigger_effect = False
                    if dialogue_i > 0:
                        Blanche_Kent_dialogue[dialogue_i - 1].hide()
                else:
                    Blanche_Kent_dialogue[dialogue_i - 1].hide()
                    Blanche_Kent_dialogue_active = False
                    dialogue_i = 0
            if itemarr[6][0].collected == True and itemarr[6][1].collected == True and itemarr[6][2].collected == True and itemarr[6][3].collected == True and itemarr[6][4].collected == True and itemarr[6][5].collected == True and Maria_Passero_dialogue_active == True:
                if Maria_once == True:
                    mazes_visited.append("Maria")
                    Maria_Passero_dialogue = Maria_dialogues()
                    Maria_once = False
                # if player hits space, move to next dialogue and clear key input
                if text_effect == False:
                    key = None
                elif text_effect == True:
                    if key == pygame.K_SPACE:
                        dialogue_i += 1
                        trigger_effect = True
                        key = None
                # show current label and hide previous label; if out of range of labels, mark as False
                if dialogue_i < len(Maria_Passero_dialogue):
                    if trigger_effect == True:
                        text_effect = False
                        # if log, don't apply effect
                        if Maria_Passero_dialogue[dialogue_i].get_text_letter_count() > 160:
                            trigger_effect = False
                            text_effect = True
                        else:
                            Maria_Passero_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                    Maria_Passero_dialogue[dialogue_i].show()
                    trigger_effect = False
                    if dialogue_i > 0:
                        Maria_Passero_dialogue[dialogue_i - 1].hide()
                else:
                    Maria_Passero_dialogue[dialogue_i - 1].hide()
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
                    pygame_gui.elements.UITextBox(f"That's someone's name.<br><br>...<br><br>Is that a date? '2309' sounds very far away.<br>>",pygame.Rect(40,30,620,620), manager, visible=0),
                    pygame_gui.elements.UITextBox(f"Who is that?<br><br>...<br>>",pygame.Rect(40,30,620,620), manager, visible=0),
                    pygame_gui.elements.UITextBox(f"Let me read the file.<br>>",pygame.Rect(40,30,620,620), manager, visible=0),
                    pygame_gui.elements.UITextBox(f"...<br>>",pygame.Rect(40,30,620,620), manager, visible=0),
                    pygame_gui.elements.UITextBox(f"It appears to be a personal log.          <br><br>...<br>Oh. I don't think I can show it to you.<br><br>Let me summarize it.<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                ]
                if poi == 1:
                    added_item = pygame_gui.elements.UITextBox(f"It says '{item1.title}.'<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    item_dialogue.append(added_item)
                    for entry in added_items:
                        item_dialogue.append(entry)
                    added_item_2 = pygame_gui.elements.UITextBox(f"...<br><br>{item1.text}<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_3 = pygame_gui.elements.UITextBox(f"...<br><br>What do you think?<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_4 = pygame_gui.elements.UITextBox(f"...<br><br>Right. One-sided conversation, sorry.<br><br>Let's see what else we can find.<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_5 = pygame_gui.elements.UITextBox(f"I'll summarize any more files we find on your screen.<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    item_dialogue.append(added_item_2)
                    item_dialogue.append(added_item_3)
                    item_dialogue.append(added_item_4)
                    item_dialogue.append(added_item_5)
                if poi == 2:
                    added_item = pygame_gui.elements.UITextBox(f"It says...<br><br>'{item2.title}.'<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    item_dialogue.append(added_item)
                    for entry in added_items:
                        item_dialogue.append(entry)
                    added_item_2 = pygame_gui.elements.UITextBox(f"...<br><br>{item2.text}<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_3 = pygame_gui.elements.UITextBox(f"...<br><br>What do you think?<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_4 = pygame_gui.elements.UITextBox(f"...<br><br>Right. One-sided conversation, sorry.<br><br>Let's see what else we can find.<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_5 = pygame_gui.elements.UITextBox(f"I'll summarize any more files we find on your screen.<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    item_dialogue.append(added_item_2)
                    item_dialogue.append(added_item_3)
                    item_dialogue.append(added_item_4)
                    item_dialogue.append(added_item_5)
                if poi == 3:
                    added_item = pygame_gui.elements.UITextBox(f"It says...<br><br>'{item3.title}.'<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    item_dialogue.append(added_item)
                    for entry in added_items:
                        item_dialogue.append(entry)
                    added_item_2 = pygame_gui.elements.UITextBox(f"...<br><br>{item3.text}<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_3 = pygame_gui.elements.UITextBox(f"...<br><br>What do you think?<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_4 = pygame_gui.elements.UITextBox(f"...<br><br>Right. One-sided conversation, sorry.<br><br>Let's see what else we can find.<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_5 = pygame_gui.elements.UITextBox(f"I'll summarize any more files we find on your screen.<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    item_dialogue.append(added_item_2)
                    item_dialogue.append(added_item_3)
                    item_dialogue.append(added_item_4)
                    item_dialogue.append(added_item_5)
                if poi == 4:
                    added_item = pygame_gui.elements.UITextBox(f"It says...<br><br>'{item4.title}.'<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    item_dialogue.append(added_item)
                    for entry in added_items:
                        item_dialogue.append(entry)
                    added_item_2 = pygame_gui.elements.UITextBox(f"...<br><br>{item4.text}<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_3 = pygame_gui.elements.UITextBox(f"...<br><br>What do you think?<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_4 = pygame_gui.elements.UITextBox(f"...<br><br>Right. One-sided conversation, sorry.<br><br>Let's see what else we can find.<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_5 = pygame_gui.elements.UITextBox(f"I'll summarize any more files we find on your screen.<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    item_dialogue.append(added_item_2)
                    item_dialogue.append(added_item_3)
                    item_dialogue.append(added_item_4)
                    item_dialogue.append(added_item_5)
                if poi == 5:
                    added_item = pygame_gui.elements.UITextBox(f"It says...<br><br>'{item5.title}.'<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    item_dialogue.append(added_item)
                    for entry in added_items:
                        item_dialogue.append(entry)
                    added_item_2 = pygame_gui.elements.UITextBox(f"...<br><br>{item5.text}<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_3 = pygame_gui.elements.UITextBox(f"...<br><br>What do you think?<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_4 = pygame_gui.elements.UITextBox(f"...<br><br>Right. One-sided conversation, sorry.<br><br>Let's see what else we can find.<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_5 = pygame_gui.elements.UITextBox(f"I'll summarize any more files we find on your screen.<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    item_dialogue.append(added_item_2)
                    item_dialogue.append(added_item_3)
                    item_dialogue.append(added_item_4)
                    item_dialogue.append(added_item_5)
                if poi == 6:
                    added_item = pygame_gui.elements.UITextBox(f"It says...<br><br>'{item6.title}.'<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    item_dialogue.append(added_item)
                    for entry in added_items:
                        item_dialogue.append(entry)
                    added_item_2 = pygame_gui.elements.UITextBox(f"...<br><br>{item6.text}<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_3 = pygame_gui.elements.UITextBox(f"...<br><br>What do you think?<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_4 = pygame_gui.elements.UITextBox(f"...<br><br>Right. One-sided conversation, sorry.<br><br>Let's see what else we can find.<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    added_item_5 = pygame_gui.elements.UITextBox(f"I'll summarize any more files we find on your screen.<br>>",pygame.Rect(40,30,620,620), manager, visible=0)
                    item_dialogue.append(added_item_2)
                    item_dialogue.append(added_item_3)
                    item_dialogue.append(added_item_4)
                    item_dialogue.append(added_item_5)
            # if player hits space, move to next dialogue and clear key input
            if text_effect == False:
                key = None
            elif text_effect == True:
                if key == pygame.K_SPACE:
                    dialogue_i += 1
                    trigger_effect = True
                    key = None
            # show current label and hide previous label; if out of range of labels, mark as False
            if dialogue_i < len(item_dialogue):
                if trigger_effect == True:
                    text_effect = False
                    item_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                item_dialogue[dialogue_i].show()
                trigger_effect = False
                if dialogue_i > 0:
                    item_dialogue[dialogue_i - 1].hide()
            else:
                item_dialogue[dialogue_i - 1].hide()
                first_item = False
                dialogue_i = 0

        # IF FIRST MAZE ENCOUNTERED
        if gamescreen != 0 and gamescreen != 7 and first_maze == True:
            # disable movement temporarily
            UP_CHANGE = False
            DOWN_CHANGE = False
            RIGHT_CHANGE = False
            LEFT_CHANGE = False
            # if player hits space, move to next dialogue and clear key input
            if text_effect == False:
                key = None
            elif text_effect == True:
                if key == pygame.K_SPACE:
                    dialogue_i += 1
                    trigger_effect = True
                    key = None
            # show current label and hide previous label; if out of range of labels, mark as False
            if dialogue_i < len(maze_dialogue):
                if trigger_effect == True:
                    text_effect = False
                    maze_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                maze_dialogue[dialogue_i].show()
                trigger_effect = False
                if dialogue_i > 0:
                    maze_dialogue[dialogue_i - 1].hide()
            else:
                maze_dialogue[dialogue_i - 1].hide()
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
            if text_effect == False:
                key = None
            elif text_effect == True:
                if key == pygame.K_SPACE:
                    dialogue_i += 1
                    trigger_effect = True
                    key = None
            # show current label and hide previous label; if out of range of labels, mark as False
            if dialogue_i < len(node_dialogue):
                if trigger_effect == True:
                    text_effect = False
                    node_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                node_dialogue[dialogue_i].show()
                trigger_effect = False
                if dialogue_i > 0:
                    node_dialogue[dialogue_i - 1].hide()
            else:
                node_dialogue[dialogue_i - 1].hide()
                node_text = False
                return_disabled = False
                dialogue_i = 0

        # ENTRY TO NETWORK DIALOGUE
        if entry_text == True:
            # if player hits space, move to next dialogue and clear key input
            if text_effect == False:
                key = None
            elif text_effect == True:
                if key == pygame.K_SPACE:
                    dialogue_i += 1
                    trigger_effect = True
                    key = None
            # show current label and hide previous label; if out of range of labels, start game
            if dialogue_i < len(entry_dialogue):
                if trigger_effect == True:
                    text_effect = False
                    entry_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                entry_dialogue[dialogue_i].show()
                trigger_effect = False
                if dialogue_i > 0:
                    entry_dialogue[dialogue_i - 1].hide()
            else:
                entry_dialogue[dialogue_i - 1].hide()
                dialogue_i = 0
                entry_text = False

        # render player
        player.draw()

        # render version text
        if render_version_2 == True:
            pygame_gui.elements.ui_label.UILabel(pygame.rect.Rect(0,680,170,20),"MAZES_V0.4_started_apr_19", manager)
            render_version_2 = False

        # add in soundtrack buttons
        screen.blit(playpause, (670,673))
        screen.blit(vol_up, (630,670))
        screen.blit(vol_down, (600,670))
        # if playing and audio ends, loop
        if pygame.mixer.get_busy() == False and playing == True:
            soundtrack.play()

        
        # ----------- PLOT VARS -------------
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

        # update and render UI
        manager.update(dt)
        manager.draw_ui(screen)

        pygame.display.flip()

        dt = clock.tick(30) / 1000

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
            if event.type == pygame_gui.UI_TEXT_EFFECT_FINISHED:
                text_effect = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_soundtrack(pygame.mouse.get_pos(), soundtrack2)
            manager.process_events(event)

        # make screen black
        screen.fill("Black")

        # end dialogue shit
        if end_dialogue_active == True:
            if end_once == True:
                end_dialogue = end_dialogues()
                end_once = False
            # if player hits space, move to next dialogue and clear key input
            if text_effect == False:
                key = None
            elif text_effect == True:
                if key == pygame.K_SPACE:
                    dialogue_i += 1
                    trigger_effect = True
                    key = None
            # show current label and hide previous label; if out of range of labels, mark as False
            if dialogue_i < len(end_dialogue):
                if trigger_effect == True:
                    text_effect = False
                    end_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                end_dialogue[dialogue_i].show()
                trigger_effect = False
                if dialogue_i > 0:
                    end_dialogue[dialogue_i - 1].hide()
            else:
                end_dialogue[dialogue_i - 1].hide()
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
            if text_effect == False:
                key = None
            elif text_effect == True:
                if key == pygame.K_SPACE:
                    dialogue_i += 1
                    trigger_effect = True
                    key = None
            # show current label and hide previous label; if out of range of labels, mark as False
            if dialogue_i < len(goodbye_dialogue):
                if trigger_effect == True:
                    text_effect = False
                    goodbye_dialogue[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
                goodbye_dialogue[dialogue_i].show()
                trigger_effect = False
                if dialogue_i > 0:
                    goodbye_dialogue[dialogue_i - 1].hide()
            else:
                goodbye_dialogue[dialogue_i - 1].hide()
                with open('resources/pois/play.json', 'w') as playfile:
                    sett = [{"gift":True}]
                    playfile.write(json.dumps(sett))
                running = False

        # render version text
        if render_version == True:
            pygame_gui.elements.ui_label.UILabel(pygame.rect.Rect(0,680,170,20),"MAZES_V0.4_started_apr_19", manager)
            render_version = False

        # add in soundtrack buttons
        screen.blit(playpause, (670,673))
        screen.blit(vol_up, (630,670))
        screen.blit(vol_down, (600,670))
        # if playing and audio ends, loop
        if pygame.mixer.get_busy() == False and playing == True:
            soundtrack2.play()

        # update and render UI
        manager.update(dt)
        manager.draw_ui(screen)

        pygame.display.flip()

        dt = clock.tick(30) / 1000


    while start_screen:
        # basic event utilities
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False
                maze_screen = False
                running = False
            if event.type == pygame.KEYUP:
                key = event.key
            if event.type == pygame_gui.UI_TEXT_EFFECT_FINISHED:
                text_effect = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_soundtrack(pygame.mouse.get_pos(), soundtrack)

        screen.fill(WALL_COLOR)

        # if player hits space, move to next label and clear key input
        if text_effect == False:
            key = None
        elif text_effect == True:
            if key == pygame.K_SPACE:
                dialogue_i += 1
                trigger_effect = True
                key = None

        # show current label and hide previous label; if out of range of labels, start game
        if dialogue_i < len(labels):
            if trigger_effect == True and text_faster == False:
                text_effect = False
                labels[dialogue_i].set_active_effect(ENTER_TEXT_EFFECT, ENTER_TEXT_EFFECT_PARAMS)
            labels[dialogue_i].show()
            trigger_effect = False
            if dialogue_i > 0:
                labels[dialogue_i - 1].hide()
        else:
            labels[dialogue_i - 1].hide()
            # be sure to set dialogue_i back to zero!
            dialogue_i = 0
            start_screen = False
            maze_screen = True

        # render version text
        if render_version == True:
            pygame_gui.elements.ui_label.UILabel(pygame.rect.Rect(0,680,170,20),"MAZES_V0.4_started_apr_19", manager)
            render_version = False

        # add in soundtrack buttons
        screen.blit(playpause, (670,673))
        screen.blit(vol_up, (630,670))
        screen.blit(vol_down, (600,670))
        # if playing and audio ends, loop
        if pygame.mixer.get_busy() == False and playing == True:
            soundtrack.play()

        # update and render UI
        manager.update(dt)
        manager.draw_ui(screen)

        pygame.display.flip()

        dt = clock.tick(30) / 1000

pygame.quit()