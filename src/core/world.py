from opensimplex import OpenSimplex
from src.models.base import BiomeType, Location
import random
from typing import Tuple, Dict, Any

class WorldGenerator:
    def __init__(self, seed: int = None):
        self.seed = seed or random.randint(0, 1000000)
        # Create two noise generators for more varied terrain
        self.elevation_noise = OpenSimplex(seed=self.seed)
        self.moisture_noise = OpenSimplex(seed=self.seed + 1)
        
        # Configure noise parameters
        self.ELEVATION_SCALE = 0.02  # Controls terrain variation
        self.MOISTURE_SCALE = 0.015  # Controls biome variation
        
        # Biome determination matrix [elevation][moisture]
        self.BIOME_MATRIX = {
            'high': {
                'wet': BiomeType.MOUNTAIN,
                'medium': BiomeType.MOUNTAIN,
                'dry': BiomeType.DESERT
            },
            'medium': {
                'wet': BiomeType.SWAMP,
                'medium': BiomeType.FOREST,
                'dry': BiomeType.PLAINS
            },
            'low': {
                'wet': BiomeType.SWAMP,
                'medium': BiomeType.PLAINS,
                'dry': BiomeType.TUNDRA
            }
        }

    def _get_elevation(self, x: int, y: int) -> float:
        """Generate elevation value for coordinates"""
        return self.elevation_noise.noise2(x * self.ELEVATION_SCALE, y * self.ELEVATION_SCALE)

    def _get_moisture(self, x: int, y: int) -> float:
        """Generate moisture value for coordinates"""
        return self.moisture_noise.noise2(x * self.MOISTURE_SCALE, y * self.MOISTURE_SCALE)

    def _determine_biome(self, x: int, y: int) -> BiomeType:
        """Determine biome based on elevation and moisture"""
        elevation = self._get_elevation(x, y)
        moisture = self._get_moisture(x, y)
        
        # Convert noise values to categories
        elev_category = (
            'high' if elevation > 0.3 else
            'low' if elevation < -0.3 else
            'medium'
        )
        
        moist_category = (
            'wet' if moisture > 0.2 else
            'dry' if moisture < -0.2 else
            'medium'
        )
        
        return self.BIOME_MATRIX[elev_category][moist_category]

    def _generate_features(self, biome: BiomeType) -> list:
        """Generate list of features for the location based on biome"""
        # This is a simple placeholder - would be expanded based on feature specs
        features = []
        if random.random() < 0.3:  # 30% chance of having a feature
            if biome == BiomeType.FOREST:
                features.append({"type": "tree", "variant": "oak"})
            elif biome == BiomeType.MOUNTAIN:
                features.append({"type": "rock", "variant": "boulder"})
        return features

    def _generate_description(self, biome: BiomeType, features: list) -> str:
        """Generate descriptive text for the location"""
        base_desc = {
            BiomeType.FOREST: "Dense trees surround you, their branches creating a natural canopy overhead.",
            BiomeType.PLAINS: "Rolling grasslands stretch out before you, swaying gently in the breeze.",
            BiomeType.MOUNTAIN: "The rocky terrain rises sharply, offering a challenging path forward.",
            BiomeType.DESERT: "Hot sand stretches as far as the eye can see, with heat waves distorting the horizon.",
            BiomeType.SWAMP: "Murky water pools around twisted vegetation in this humid environment.",
            BiomeType.TUNDRA: "A stark, frozen landscape extends in all directions, with a bitter wind howling."
        }
        
        description = base_desc.get(biome, "You stand in an unremarkable area.")
        
        # Add feature descriptions
        for feature in features:
            if feature["type"] == "tree":
                description += f" A mighty {feature['variant']} tree stands nearby."
            elif feature["type"] == "rock":
                description += f" A large {feature['variant']} dominates the immediate area."
                
        return description

    def generate_location(self, x: int, y: int) -> Tuple[BiomeType, list, str]:
        """Generate a complete location at the given coordinates"""
        biome = self._determine_biome(x, y)
        features = self._generate_features(biome)
        description = self._generate_description(biome, features)
        
        # Add some randomization to descriptions
        if random.random() < 0.3:  # 30% chance of additional detail
            time_details = [
                "The sun hangs low on the horizon.",
                "A gentle breeze rustles through the area.",
                "The air is still and quiet here.",
                "Clouds cast shifting shadows across the landscape."
            ]
            description += f" {random.choice(time_details)}"
        
        return biome, features, description
