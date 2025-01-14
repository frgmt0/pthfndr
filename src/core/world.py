from opensimplex import OpenSimplex
from src.models.base import BiomeType, Location
import random
from typing import Tuple, Dict, Any

class WorldGenerator:
    def __init__(self, seed: int = None):
        self.seed = seed or random.randint(0, 1000000)
        self.noise_gen = OpenSimplex(seed=self.seed)
        
        # Configure noise parameters
        self.SCALE = 0.007  # Controls how zoomed in/out the noise is
        self.BIOME_THRESHOLDS = {
            (-1.0, -0.6): BiomeType.TUNDRA,
            (-0.6, -0.2): BiomeType.MOUNTAIN,
            (-0.2, 0.0): BiomeType.PLAINS,
            (0.0, 0.3): BiomeType.FOREST,
            (0.3, 0.6): BiomeType.SWAMP,
            (0.6, 1.0): BiomeType.DESERT
        }

    def _get_noise(self, x: int, y: int) -> float:
        """Generate noise value for coordinates"""
        return self.noise_gen.noise2(x * self.SCALE, y * self.SCALE)

    def _determine_biome(self, noise_val: float) -> BiomeType:
        """Convert noise value to biome type"""
        for (min_val, max_val), biome in self.BIOME_THRESHOLDS.items():
            if min_val <= noise_val <= max_val:
                return biome
        return BiomeType.PLAINS  # Default biome

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
        noise_val = self._get_noise(x, y)
        biome = self._determine_biome(noise_val)
        features = self._generate_features(biome)
        description = self._generate_description(biome, features)
        
        return biome, features, description
