from enum import Enum

class States(Enum):
    SELECTED = "selected"
    IN_GAME = "ingame"
    PAUSE = "pause"
    MAIN_MENU = "mainmenu"
    DRAGGING_ANIMAL = "dragging_animal"