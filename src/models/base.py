from tortoise import fields, models
from enum import Enum

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

    class Meta:
        table = "game_states"

class Location(models.Model):
    id = fields.IntField(pk=True)
    x = fields.IntField()
    y = fields.IntField()
    biome_type = fields.CharEnumField(BiomeType)
    description = fields.TextField()
    features = fields.JSONField()
    discovered = fields.BooleanField(default=False)
    
    class Meta:
        table = "locations"
        unique_together = (("x", "y"),)
