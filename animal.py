import random

class Animal:
    def __init__(self, id, enclosure_id, x, y, species, age = 0):
        # Identity
        self.animal_id = id
        self.age = age
        self.species = species
        self.sex = random.choice(["male", "female"])
        self.age_stage = "baby"
        self.name = None

        # Position and movement
        self.x = x
        self.y = y
        self.target_coords = (x, y)
        self.speed = 2.0
        self.direction = "south"

        # Enclosure
        self.enclosure_id = enclosure_id
        self.home_zone = None

        # Physical stats
        self.health = 100.0
        self.max_health  = 100.0
        self.hunger = 50.0 # 0 - 100, higher = more hungry
        self.thirst = 50.0
        self.energy = 100.0
        self.size = 1.0

        #Psychological stats
        self.happiness = 100
        self.stress = 0.0
        self.boredom = 0.0
        self.social_need = 50.0

        # Behaviour state  
        self.state = "idle"
        self.activity_timer = 0.0
        self.last_fed = 0
        self.last_drunk = 0
        self.last_slept = 0