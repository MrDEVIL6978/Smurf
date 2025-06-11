
class FishingRod:
    def __init__(self, name, price, durability, efficiency, luck):
        self.name = name
        self.price = price
        self.durability = durability
        self.max_durability = durability
        self.efficiency = efficiency
        self.luck = luck

class FishingItem:

    def __init__(self, name, rarity, rarity_weight, price, locations):
        self.name = name
        self.rarity = rarity
        self.rarity_weight = rarity_weight
        self.price = price
        self.locations = locations


class FishingLocation:

    def __init__(self, name, difficulty, min_level, description):
        self.name = name
        self.difficulty = difficulty
        self.min_level = min_level
        self.description = description


class FishingBait:
    def __init__(self, name, efficiency, rarity, rarity_weight, price, locations):
        self.name = name
        self.efficiency = efficiency
        self.rarity = rarity
        self.rarity_weight = rarity_weight
        self.price = price
        self.locations = locations

class FishingAccessory:
    def __init__(self, name, price, efficiency, luck, catch_bonus):
        self.name = name
        self.price = price
        self.efficiency = efficiency
        self.luck = luck
        self.catch_bonus = catch_bonus


FISHING_RODS = {
    "Wooden Rod": {
        "durability": 50,
        "efficiency": 1,
        "luck": 1,
        "price": 100
    },
    "Bamboo Rod": {
        "durability": 75,
        "efficiency": 1.2,
        "luck": 1.1,
        "price": 250
    },
    "Fiberglass Rod": {
        "durability": 100,
        "efficiency": 1.5,
        "luck": 1.2,
        "price": 500
    },
    "Carbon Fiber Rod": {
        "durability": 150,
        "efficiency": 1.8,
        "luck": 1.3,
        "price": 1000
    },
    "Enchanted Rod": {
        "durability": 200,
        "efficiency": 2,
        "luck": 1.5,
        "price": 2500
    },
    "Deep Sea Rod": {
        "durability": 250,
        "efficiency": 2.2,
        "luck": 1.4,
        "price": 5000
    },
    "Celestial Rod": {
        "durability": 500,
        "efficiency": 2.5,
        "luck": 2,
        "price": 10000
    },
    "Void Fishing Rod": {
        "durability": 1000,
        "efficiency": 3,
        "luck": 2.5,
        "price": 25000
    }
}
FISHING_ITEMS = {
    # Common Freshwater Fish
    "Perch": {
        "rarity": "Common",
        "rarity_weight": 100,
        "price": 5,
        "locations": ["Calm Lake", "Rapid River"]
    },
    "Bluegill": {
        "rarity": "Common",
        "rarity_weight": 95,
        "price": 4,
        "locations": ["Calm Lake", "Enchanted Pond"]
    },
    "Carp": {
        "rarity": "Common",
        "rarity_weight": 90,
        "price": 6,
        "locations": ["Calm Lake", "Rapid River"]
    },
    "Catfish": {
        "rarity": "Uncommon",
        "rarity_weight": 75,
        "price": 15,
        "locations": ["Calm Lake", "Rapid River", "Underwater Caves"]
    },

    # Common Saltwater Fish
    "Mackerel": {
        "rarity": "Common",
        "rarity_weight": 85,
        "price": 8,
        "locations": ["Open Ocean", "Coral Reef"]
    },
    "Herring": {
        "rarity": "Common",
        "rarity_weight": 80,
        "price": 7,
        "locations": ["Open Ocean", "Deep Sea"]
    },
    "Cod": {
        "rarity": "Common",
        "rarity_weight": 75,
        "price": 10,
        "locations": ["Open Ocean", "Deep Sea"]
    },

    # Uncommon Fish
    "Bass": {
        "rarity": "Uncommon",
        "rarity_weight": 70,
        "price": 20,
        "locations": ["Calm Lake", "Rapid River"]
    },
    "Trout": {
        "rarity": "Uncommon",
        "rarity_weight": 65,
        "price": 25,
        "locations": ["Rapid River", "Crystal Cave"]
    },
    "Salmon": {
        "rarity": "Uncommon",
        "rarity_weight": 60,
        "price": 30,
        "locations": ["Rapid River", "Deep Sea"]
    },
    "Red Snapper": {
        "rarity": "Uncommon",
        "rarity_weight": 55,
        "price": 35,
        "locations": ["Coral Reef", "Open Ocean"]
    },

    # Rare Fish
    "Swordfish": {
        "rarity": "Rare",
        "rarity_weight": 40,
        "price": 100,
        "locations": ["Open Ocean", "Deep Sea"]
    },
    "Tuna": {
        "rarity": "Rare",
        "rarity_weight": 35,
        "price": 120,
        "locations": ["Open Ocean", "Deep Sea"]
    },
    "Mahi-Mahi": {
        "rarity": "Rare",
        "rarity_weight": 30,
        "price": 150,
        "locations": ["Open Ocean", "Coral Reef"]
    },
    "Sturgeon": {
        "rarity": "Rare",
        "rarity_weight": 25,
        "price": 200,
        "locations": ["Rapid River", "Deep Sea"]
    },

    # Epic Fish
    "Giant Squid": {
        "rarity": "Epic",
        "rarity_weight": 15,
        "price": 500,
        "locations": ["Deep Sea", "The Void"]
    },
    "Great White Shark": {
        "rarity": "Epic",
        "rarity_weight": 10,
        "price": 1000,
        "locations": ["Open Ocean", "Shark Trench"]
    },
    "Blue Marlin": {
        "rarity": "Epic",
        "rarity_weight": 8,
        "price": 1500,
        "locations": ["Open Ocean", "Deep Sea"]
    },

    # Legendary Fish
    "Kraken Tentacle": {
        "rarity": "Legendary",
        "rarity_weight": 5,
        "price": 5000,
        "locations": ["Kraken's Lair"]
    },
    "Golden Koi": {
        "rarity": "Legendary",
        "rarity_weight": 4,
        "price": 10000,
        "locations": ["Enchanted Pond"]
    },
    "Loch Ness Monster": {
        "rarity": "Legendary",
        "rarity_weight": 3,
        "price": 20000,
        "locations": ["Crystal Cave", "The Void"]
    },

    # Mythical Fish
    "Mermaid's Scale": {
        "rarity": "Mythical",
        "rarity_weight": 2,
        "price": 50000,
        "locations": ["Sunken City", "Underwater Ruins"]
    },
    "Phoenix Fish": {
        "rarity": "Mythical",
        "rarity_weight": 1,
        "price": 100000,
        "locations": ["Underwater Volcano"]
    },

    # Trash Items
    "Seaweed": {
        "rarity": "Common",
        "rarity_weight": 120,
        "price": 1,
        "locations": ["Calm Lake", "Rapid River", "Open Ocean", "Deep Sea"]
    },
    "Driftwood": {
        "rarity": "Common",
        "rarity_weight": 110,
        "price": 2,
        "locations": ["Calm Lake", "Rapid River", "Open Ocean"]
    },
    "Old Boot": {
        "rarity": "Common",
        "rarity_weight": 105,
        "price": 1,
        "locations": ["Calm Lake", "Rapid River", "Sunken Shipwreck"]
    },
    "Rusty Can": {
        "rarity": "Common",
        "rarity_weight": 100,
        "price": 1,
        "locations": ["Calm Lake", "Rapid River", "Sunken Shipwreck"]
    },

    # Treasure Items
    "Message in a Bottle": {
        "rarity": "Uncommon",
        "rarity_weight": 50,
        "price": 50,
        "locations": ["Open Ocean", "Sunken Shipwreck"]
    },
    "Ancient Coin": {
        "rarity": "Rare",
        "rarity_weight": 20,
        "price": 500,
        "locations": ["Underwater Ruins", "Sunken City"]
    },
    "Treasure Chest": {
        "rarity": "Epic",
        "rarity_weight": 5,
        "price": 5000,
        "locations": ["Sunken Shipwreck", "Underwater Ruins", "Sunken City"]
    },

    # Special Items
    "Glowing Algae": {
        "rarity": "Uncommon",
        "rarity_weight": 45,
        "price": 100,
        "locations": ["Deep Sea", "Underwater Caves"]
    },
    "Enchanted Coral": {
        "rarity": "Rare",
        "rarity_weight": 15,
        "price": 1000,
        "locations": ["Coral Reef", "Enchanted Pond"]
    },
    "Void Essence": {
        "rarity": "Legendary",
        "rarity_weight": 1,
        "price": 50000,
        "locations": ["The Void"]
    }
}

FISHING_LOCATIONS = {
    "Calm Lake": {
        "difficulty": 1,
        "min_level": 1,
        "description": "A peaceful lake teeming with basic fish."
    },
    "Rapid River": {
        "difficulty": 3,
        "min_level": 5,
        "description": "A fast-flowing river with stronger currents."
    },
    "Deep Sea": {
        "difficulty": 5,
        "min_level": 10,
        "description": "The depths of the ocean, home to mysterious creatures."
    },
    "Open Ocean": {
        "difficulty":
        7,
        "min_level":
        15,
        "description":
        "The vast expanse of the sea, where powerful predators roam."
    },
    "Enchanted Pond": {
        "difficulty": 9,
        "min_level": 20,
        "description": "A magical pond shimmering with ancient energy."
    },
    "Sunken Shipwreck": {
        "difficulty": 6,
        "min_level": 12,
        "description": "The remains of a wrecked ship, now home to scavengers."
    },
    "Underwater Ruins": {
        "difficulty":
        8,
        "min_level":
        18,
        "description":
        "The ruins of an ancient civilization, lost beneath the waves."
    },
    "Coral Reef": {
        "difficulty": 4,
        "min_level": 8,
        "description": "A vibrant reef bustling with colorful life."
    },
    "Underwater Caves": {
        "difficulty": 6,
        "min_level": 13,
        "description":
        "A network of dark caves, home to bioluminescent creatures."
    },
    "Shark Trench": {
        "difficulty":
        9,
        "min_level":
        22,
        "description":
        "A deep trench where only the bravest (or craziest) dare to fish."
    },
    "Kraken's Lair": {
        "difficulty":
        11,
        "min_level":
        25,
        "description":
        "The legendary lair of the Kraken, a place of immense danger and reward."
    },
    "Celestial Pond": {
        "difficulty":
        13,
        "min_level":
        30,
        "description":
        "A mystical pond bathed in starlight, said to hold fish touched by the cosmos."
    },
    "The Void": {
        "difficulty":
        15,
        "min_level":
        35,
        "description":
        "A rift in reality, where the laws of nature bend and break."
    },
    "Crystal Cave": {
        "difficulty":
        10,
        "min_level":
        23,
        "description":
        "A hidden cave filled with glowing crystals, attracting unique fish."
    },
    "Sunken City": {
        "difficulty": 12,
        "min_level": 28,
        "description":
        "The remnants of a once-great city, now claimed by the sea."
    },
    "Underwater Volcano": {
        "difficulty":
        14,
        "min_level":
        33,
        "description":
        "An active underwater volcano, spewing forth heat and rare minerals that attract unusual life forms."
    }
}
FISHING_BAITS = {
    "dough balls": {
        "efficiency": 1.1,
        "rarity": "Common",
        "rarity_weight": 50,
        "price": 5,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    },
    "worm": {
        "efficiency": 1.2,
        "rarity": "Common",
        "rarity_weight": 90,
        "price": 10,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    },
    "Snail": {
        "efficiency": 1.4,
        "rarity": "Common",
        "rarity_weight": 120,
        "price": 2,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    },
    "Crab": {
        "efficiency": 1.6,
        "rarity": "Common",
        "rarity_weight": 130,
        "price": 2,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    },
    "Shrimp": {
        "efficiency": 1.8,
        "rarity": "Common",
        "rarity_weight": 140,
        "price": 2,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    },
    "fish food": {
        "efficiency": 2,
        "rarity": "UnCommon",
        "rarity_weight": 150,
        "price": 2,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    },
    "Squid": {
        "efficiency": 2.2,
        "rarity": "UnCommon",
        "rarity_weight": 160,
        "price": 2,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    },
    "Octopus": {
        "efficiency": 2.4,
        "rarity": "UnCommon",
        "rarity_weight": 170,
        "price": 2,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    },
    "Clownfish": {
        "efficiency": 2.6,
        "rarity": "UnCommon",
        "rarity_weight": 180,
        "price": 2,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    },
    "Sea Urchin": {
        "efficiency": 2.8,
        "rarity": "rare",
        "rarity_weight": 200,
        "price": 2,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    },
    "Jellyfish": {
        "efficiency": 3,
        "rarity": "rare",
        "rarity_weight": 230,
        "price": 2,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    },
    "meat balls": {
        "efficiency": 3.2,
        "rarity": "rare",
        "rarity_weight": 250,
        "price": 2,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    },
    "Human Cage": {
        "efficiency": 3.5,
        "rarity": "Epic",
        "rarity_weight": 260,
        "price": 2,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    },
    "magnet": {
        "efficiency": 3.7,
        "rarity": "Epic",
        "rarity_weight": 270,
        "price": 2,
        "locations": ["Calm Lake", "Rapid River", "Deep Sea", "Open Ocean"]
    }
}
FISHING_ACCESSORIES = {
    "Lucky Charm": {
        "luck": 1.1,
        "efficiency": 1.0,
        "catch_bonus": 0,
        "special": "Increases chance of rare fish (Showcase only)",
        "price": 500
    },
    "Fishing Hat": {
        "luck": 1.05,
        "efficiency": 1.05,
        "catch_bonus": 1,
        "special": "Protects from sunburn (Showcase only)",
        "price": 750
    },
    "Waterproof Gloves": {
        "luck": 1.0,
        "efficiency": 1.1,
        "catch_bonus": 1,
        "special": "Improves grip on wet rods (Showcase only)",
        "price": 1000
    },
    "Fishing Vest": {
        "luck": 1.05,
        "efficiency": 1.15,
        "catch_bonus": 2,
        "special": "Extra storage for lures (Showcase only)",
        "price": 1500
    },
    "Depth Finder": {
        "luck": 1.1,
        "efficiency": 1.2,
        "catch_bonus": 2,
        "special": "Locate fish more easily (Showcase only)",
        "price": 2000
    },
    "Lure Case": {
        "luck": 1.15,
        "efficiency": 1.1,
        "catch_bonus": 3,
        "special": "Organize and protect lures (Showcase only)",
        "price": 2500
    },
    "Enchanted Lure": {
        "luck": 1.2,
        "efficiency": 1.1,
        "catch_bonus": 3,
        "special": "Attracts rare fish (Showcase only)",
        "price": 5000
    },
    "Golden Hook": {
        "luck": 1.3,
        "efficiency": 1.2,
        "catch_bonus": 4,
        "special": "Never rusts (Showcase only)",
        "price": 10000
    },
    "Poseidon's Blessing": {
        "luck": 1.4,
        "efficiency": 1.3,
        "catch_bonus": 5,
        "special": "Calms the waters (Showcase only)",
        "price": 25000
    },
    "Cosmic Fishing Line": {
        "luck": 1.5,
        "efficiency": 1.4,
        "catch_bonus": 6,
        "special": "Unbreakable line (Showcase only)",
        "price": 50000
    }
}