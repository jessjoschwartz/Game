import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 7
GAME_HEIGHT = 7
LADDER = None
BEAST = None
PRINCESS = None
LOGO = None
DUNKAROOS = None
GUSHERS = None
HEART = None
#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True
    name = "rock"

class TallTree(GameElement):
    IMAGE = "TallTree"
    SOLID = True
    name = "tree"

    def __init__(self):
        GameElement.__init__(self)

    def interact(self, player):
        if player.inventory.get(self.name):
            player.inventory[self.name] += 1
        else:
            player.inventory[self.name] = 1

        GAME_BOARD.draw_msg("You just acquired a tree! You have %d trees!" % player.inventory[self.name])
        if player.inventory[self.name] == 3:
            GAME_BOARD.draw_msg("You unlocked the ladder!  Press the Spacebar to climb the ladder.")

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    name = "key"

    def interact(self, player):
        player.inventory[self.name] = 1
        GAME_BOARD.draw_msg("You just acquired a key!")

class Axe(GameElement):
    IMAGE = "Axe"
    SOLID = False
    name = "axe"

    def __init__(self):
        GameElement.__init__(self)

    def interact(self, player):
        player.inventory[self.name] = 1
        GAME_BOARD.draw_msg("You just acquired an axe! You can now cut down trees!") 
        print player.inventory

class Ladder(GameElement):
    IMAGE = "Ladder"
    SOLID = False
    name = "ladder"

class Beast(GameElement):
    IMAGE = "Beast"
    SOLID = True
    name = "beast"

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True
    name = "wall"

class Logo(GameElement):
    IMAGE = "Hackbright"
    SOLID = False
    name = "logo"

    def interact(self, player):
        PLAYER.inventory[self.name] = 1
        GAME_BOARD.draw_msg("Bring the letter to the princess to win her heart!")

class Teacup(GameElement):
    IMAGE = "Teacup"
    SOLID = True
    name = "teacup"

    def interact(self, player):
        global PRINCESS
        GAME_BOARD.del_el(PRINCESS.x, PRINCESS.y)
        GAME_BOARD.draw_msg("You touched the TEACUP OF DEATH.  You have killed the princess.")
        PRINCESS = None

class Character(GameElement):
    IMAGE = "Girl" 
    name = "heroine"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = {}

    def next_pos(self, direction):
        print direction
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        elif direction == "space":
            return (self.x, self.y-3)
        return None

    def interact(self, player):
        if PLAYER.inventory.get("logo"):
            for x in range(7):
                for y in range(7):
                    GAME_BOARD.set_el(x, y, HEART)

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory[self] = 1
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % len(player.inventory)) 

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True
    name = "chest"

    def interact(self, player):
        if player.inventory.get("key"):
            GAME_BOARD.draw_msg("You have unlocked the chest!  Inside is...A HACKBRIGHT ACCEPTANCE LETTER!")
            GAME_BOARD.del_el(0, 1)
            GAME_BOARD.set_el(0, 1, LOGO)

class Snack(GameElement):
    IMAGE = "Dunkaroos"
    SOLID = False
    name = "dunkaroos"

    def interact(self, player):
        player.inventory[self.name] = 1
        if player.inventory.get("dunkaroos"):
            GAME_BOARD.draw_msg("The beast is allergic to Dunkaroos.  He attacks the Princess in a ferocious rage and kills her.")
            GAME_BOARD.del_el(6, 0)
            GAME_BOARD.del_el(3, 0)
            GAME_BOARD.del_el(4, 1)
            GAME_BOARD.set_el(6, 0, BEAST)
        elif player.inventory.get("gushers"):
            GAME_BOARD.draw_msg("The beast loooooooooves Gushers!  It is now your friend.  Press ENTER to hear its advice.")
            GAME_BOARD.del_el(2, 1)

class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = True
    name = "heart"

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

    wall_positions = [
            (0, 3),
            (1, 3), 
            (2, 3),
            (3, 3),
            (4, 3),
            (5, 3),
            (6, 3)
        ]

    wall_sections = []

    for pos in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0], pos[1], wall)
        wall_sections.append(wall)

    tree_positions = [
            (0, 4),
            (3, 4),
            (6, 4)
        ]

    trees = []

    for pos in tree_positions:
        talltree = TallTree()
        GAME_BOARD.register(talltree)
        GAME_BOARD.set_el(pos[0], pos[1], talltree)
        trees.append(talltree)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(0, 6, key)

    axe = Axe()
    GAME_BOARD.register(axe)
    GAME_BOARD.set_el(6, 6, axe)

    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(0, 1, chest)

    global LOGO
    LOGO = Logo()
    GAME_BOARD.register(LOGO)
    #GAME_BOARD.set_el(0, 0, logo)

    global PRINCESS
    PRINCESS = Character()
    PRINCESS.IMAGE = "Princess"
    PRINCESS.name = "Princess"
    GAME_BOARD.register(PRINCESS)
    GAME_BOARD.set_el(6, 0, PRINCESS)    

    teacup = Teacup()
    GAME_BOARD.register(teacup)
    GAME_BOARD.set_el(2, 6, teacup)

    global LADDER
    LADDER = Ladder()
    GAME_BOARD.register(LADDER)

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(3, 6, PLAYER)

    global BEAST 
    BEAST = Beast()
    GAME_BOARD.register(BEAST)

    global DUNKAROOS 
    DUNKAROOS = Snack()
    GAME_BOARD.register(DUNKAROOS)

    global GUSHERS
    GUSHERS = Snack()
    GUSHERS.IMAGE = "Gushers"
    GUSHERS.name = "gushers"
    GAME_BOARD.register(GUSHERS)

    global HEART
    HEART = Heart()
    GAME_BOARD.register(HEART)

    GAME_BOARD.draw_msg("Win the princess' heart!  Hint: don't forget the key.")

def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"
    if KEYBOARD[key.SPACE]:
        direction = "space"

    if KEYBOARD[key.ENTER] and not PLAYER.inventory.get("gushers"):
        GAME_BOARD.draw_msg("The beast has the munchies.  Maybe you could choose a snack to give it?")
        GAME_BOARD.set_el(2, 1, DUNKAROOS)
        GAME_BOARD.set_el(4, 1, GUSHERS)
    elif KEYBOARD[key.ENTER] and PLAYER.inventory.get("gushers"):
        GAME_BOARD.draw_msg("The gift to win the Princess' heart is in the chest!  Unlock it and give it to her!")

    if direction == None:
        return

    next_location = PLAYER.next_pos(direction) 
    next_x = next_location[0]
    next_y = next_location[1]

    if direction and 0 <= next_x < GAME_WIDTH and 0 <= next_y < GAME_HEIGHT:
        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

            # if PLAYER.inventory.get("tree") == 3:
            #     GAME_BOARD.set_el(3, 4, LADDER)
            #     GAME_BOARD.draw_msg("Go to the ladder and press Spacebar to climb!")

            if existing_el.name == "tree" and PLAYER.inventory["axe"]:
                GAME_BOARD.del_el(next_x, next_y)

        if PLAYER.inventory.get("tree") == 3 and PLAYER.y > 3 and PRINCESS:
            GAME_BOARD.set_el(3, 4, LADDER)
            GAME_BOARD.draw_msg("Go to the ladder and press Spacebar to climb!")

        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)

        if direction == "space" and LADDER:
                GAME_BOARD.draw_msg("First, you must defeat this FEROCIOUS BEAST.  Press ENTER to find out how.")
                GAME_BOARD.set_el(3, 0, BEAST)


