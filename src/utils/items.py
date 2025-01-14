from typing import Dict, Any
from src.models.base import ItemType
import random

# Expanded item prefixes and suffixes for more variety
ITEM_NAME_PREFIXES = [
    "Ancient", "Enchanted", "Rusted", "Glowing", "Cursed", 
    "Mystical", "Dark", "Blessed", "Celestial", "Infernal",
    "Forgotten", "Sacred", "Corrupted", "Divine", "Demonic"
]

ITEM_NAME_ROOTS = {
    ItemType.WEAPON: [
        "Sword", "Bow", "Dagger", "Staff", "Axe", "Spear",
        "Mace", "Warhammer", "Blade", "Scythe", "Crossbow"
    ],
    ItemType.ARMOR: [
        "Helm", "Chestplate", "Gauntlets", "Boots", "Shield",
        "Cloak", "Robe", "Bracers", "Greaves", "Pauldrons"
    ],
    ItemType.POTION: [
        "Elixir", "Potion", "Brew", "Tonic", "Draught",
        "Philter", "Mixture", "Solution", "Concoction", "Essence"
    ],
    ItemType.TOOL: [
        "Pickaxe", "Shovel", "Hammer", "Chisel", "Compass",
        "Map", "Rope", "Lantern", "Key", "Lock"
    ],
    ItemType.TREASURE: [
        "Ring", "Amulet", "Crown", "Gem", "Crystal",
        "Medallion", "Chalice", "Scepter", "Relic", "Artifact"
    ]
}

ITEM_NAME_SUFFIXES = [
    "of Power", "of the Ancients", "of Frost", "of Flames", "of Shadows",
    "of Light", "of Wisdom", "of Speed", "of Protection", "of Life",
    "of Death", "of Time", "of Space", "of the Moon", "of the Sun"
]

ITEM_DESCRIPTION_TEMPLATES = [
    "This {rarity} {item_type} radiates with {energy} energy.",
    "The surface of this {item_type} is covered in {pattern} engravings.",
    "A {intensity} {element} aura emanates from this {rarity} artifact.",
    "This {rarity} {item_type} feels {weight} in your hands.",
    "The craftsmanship of this {item_type} is truly {quality}."
]

DESCRIPTION_ATTRIBUTES = {
    "energy": ["ancient", "mystical", "dark", "divine", "elemental", "cosmic"],
    "pattern": ["intricate", "runic", "celestial", "geometric", "flowing", "chaotic"],
    "intensity": ["faint", "pulsing", "blinding", "shimmering", "swirling"],
    "element": ["frost", "fire", "shadow", "light", "lightning", "void"],
    "weight": ["surprisingly light", "perfectly balanced", "unnaturally heavy", "weightless"],
    "quality": ["exceptional", "masterful", "legendary", "otherworldly", "unmatched"]
}

def generate_item_name(item_type: ItemType) -> str:
    """Generate a random item name based on type"""
    prefix = random.choice(ITEM_NAME_PREFIXES)
    root = random.choice(ITEM_NAME_ROOTS[item_type])
    suffix = random.choice(ITEM_NAME_SUFFIXES)
    return f"{prefix} {root} {suffix}"

def generate_item_description(item_type: ItemType, rarity: str) -> str:
    """Generate a random item description"""
    template = random.choice(ITEM_DESCRIPTION_TEMPLATES)
    attributes = {
        "rarity": rarity,
        "item_type": item_type.value,
        "energy": random.choice(DESCRIPTION_ATTRIBUTES["energy"]),
        "pattern": random.choice(DESCRIPTION_ATTRIBUTES["pattern"]),
        "intensity": random.choice(DESCRIPTION_ATTRIBUTES["intensity"]),
        "element": random.choice(DESCRIPTION_ATTRIBUTES["element"]),
        "weight": random.choice(DESCRIPTION_ATTRIBUTES["weight"]),
        "quality": random.choice(DESCRIPTION_ATTRIBUTES["quality"])
    }
    return template.format(**attributes)

def generate_item_properties(item_type: ItemType, rarity_multiplier: float = 1.0) -> Dict[str, Any]:
    """Generate properties based on item type and rarity"""
    base_properties = {
        ItemType.WEAPON: {
            "damage": random.uniform(5, 15) * rarity_multiplier,
            "attack_speed": random.uniform(0.5, 1.5),
            "durability": random.uniform(50, 100) * rarity_multiplier
        },
        ItemType.ARMOR: {
            "defense": random.uniform(2, 10) * rarity_multiplier,
            "weight": random.uniform(1.0, 5.0),
            "durability": random.uniform(50, 100) * rarity_multiplier
        },
        ItemType.POTION: {
            "potency": random.uniform(1, 10) * rarity_multiplier,
            "duration": random.uniform(10, 60),
            "side_effects": random.random() < 0.3
        },
        ItemType.TOOL: {
            "efficiency": random.uniform(1, 5) * rarity_multiplier,
            "durability": random.uniform(30, 80) * rarity_multiplier,
            "versatility": random.uniform(1, 3)
        },
        ItemType.TREASURE: {
            "value": random.uniform(10, 100) * rarity_multiplier,
            "age": random.uniform(100, 1000),
            "magical": random.random() < 0.5
        }
    }
    
    return base_properties.get(item_type, {})
