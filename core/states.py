from enum import Enum

class States(Enum):
    SELECTED = "selected"
    IN_GAME = "ingame"
    PAUSE = "pause"
    MAIN_MENU = "main_menu"
    DRAGGING_ANIMAL = "dragging_animal"
    EMPTY = "empty"
    ENCLOSURE = "enclosure"
    ANIMAL = "animal"
    TRANSITION = "transition"