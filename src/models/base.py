from tortoise import fields, models
from enum import Enum
from typing import Optional

class ItemType(str, Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    POTION = "potion"
    TOOL = "tool"
    TREASURE = "treasure"
    KEY = "key"

class BiomeType(str, Enum):
    FOREST = "FRST"
    PLAINS = "PLNS" 
    MOUNTAIN = "MNTN"
    DESERT = "DSRT"
    SWAMP = "SWMP"
    TUNDRA = "TNDR"

class GameState(models.Model):
    id = fields.IntField(pk=True)
    seed = fields.IntField()
    current_position = fields.JSONField()  # {x: int, y: int}
    current_biome = fields.CharEnumField(BiomeType)
    inventory = fields.JSONField(default=dict)
    health = fields.IntField(default=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    weather = fields.CharField(max_length=20, null=True)  # Current weather

    class Meta:
        table = "game_states"

class Location(models.Model):
    id = fields.IntField(pk=True)
    x = fields.IntField()
    y = fields.IntField()
    biome_type = fields.CharEnumField(BiomeType)
    description = fields.TextField()
    features = fields.JSONField()
    weather = fields.CharField(max_length=20, null=True)  # Current weather
    discovered = fields.BooleanField(default=False)
    
    class Meta:
        table = "locations"
        unique_together = (("x", "y"),)

class Item(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    item_type = fields.CharEnumField(ItemType)
    description = fields.TextField()
    properties = fields.JSONField(default=dict)  # For type-specific properties
    game_state = fields.ForeignKeyField('models.GameState', related_name='items')
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "items"
