from animals import animal_manager
from enclosures import enclosure_manager
from objects import object_manager
import json

class SaveManager:
    def __init__(self, game_clock, animalManager, enclosureManager, objectManager, player):
        self.game_clock = game_clock
        self.animal_manager = animalManager
        self.enclosure_manager = enclosureManager
        self.object_manager = objectManager
        self.player = player

    def save(self, file_path = "save.json"):
        data = {
            "clock": self.game_clock.to_dict(),
            "animal_manager": self.animal_manager.to_dict(),
            "enclosure_manager": self.enclosure_manager.to_dict(),
            "object_manager": self.object_manager.to_dict(),

            "player": self.player.to_dict()
        }
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile, indent= 2)

    def load(self, file_path = "save.json"):
        with open(file_path, "r") as json_file:
            data = json.load(json_file)

        # First pass: reconstruct all objects from data
        self.game_clock.from_dict(data["clock"])
        self.animal_manager.from_dict(data["animal_manager"])
        self.enclosure_manager.from_dict(data["enclosure_manager"])
        self.object_manager.from_dict(data["object_manager"])
        self.player.from_dict(data["player"])

        # Second pass: relink references
        self.re_link_references()

    def re_link_references(self):
        pass