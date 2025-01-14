from typing import Dict, Any
from src.models.base import ItemType

# Define base properties for each item type
ITEM_DEFINITIONS = {
    # Fish and other food items
    "Fish": {
        "type": ItemType.TREASURE,
        "properties": {
            "value": 10.00,
            "edible": True,
            "health_restore": 15
        },
        "description": "A fresh fish that could make a good meal"
    },
    "Berry": {
        "type": ItemType.TREASURE,
        "properties": {
            "value": 5.00,
            "edible": True,
            "health_restore": 5
        },
        "description": "A sweet wild berry"
    },
    
    # Weapons
    "Rusty Sword": {
        "type": ItemType.WEAPON,
        "properties": {
            "damage": 8,
            "durability": 50,
            "value": 25.00
        },
        "description": "An old sword showing signs of wear"
    },
    "Hunter's Bow": {
        "type": ItemType.WEAPON,
        "properties": {
            "damage": 12,
            "range": 50,
            "value": 45.00
        },
        "description": "A well-crafted wooden bow"
    },

    # Tools
    "Wooden Pickaxe": {
        "type": ItemType.TOOL,
        "properties": {
            "mining_power": 5,
            "durability": 30,
            "value": 15.00
        },
        "description": "A basic tool for mining"
    },
    
    # Potions
    "Health Potion": {
        "type": ItemType.POTION,
        "properties": {
            "heal_amount": 50,
            "value": 30.00
        },
        "description": "A red potion that restores health"
    },

    # Treasures
    "Gold Ring": {
        "type": ItemType.TREASURE,
        "properties": {
            "value": 100.00,
            "magical": False
        },
        "description": "A simple but valuable gold ring"
    },
    "Ancient Coin": {
        "type": ItemType.TREASURE,
        "properties": {
            "value": 50.00,
            "age": 1000
        },
        "description": "A coin from a long-lost civilization"
    }
}

def get_item_definition(item_name: str) -> Dict[str, Any]:
    """Get the definition for a specific item"""
    return ITEM_DEFINITIONS.get(item_name, {})
