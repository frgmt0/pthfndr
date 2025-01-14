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
        self.ELEVATION_SCALE = 0.05  # Increased for more terrain variation
        self.MOISTURE_SCALE = 0.03   # Increased for more moisture variation
        
        # Add some random offset to prevent grid-like patterns
        self.x_offset = random.uniform(-1000, 1000)
        self.y_offset = random.uniform(-1000, 1000)
        
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
        # Add offsets and multiple noise layers for more variation
        primary = self.elevation_noise.noise2((x + self.x_offset) * self.ELEVATION_SCALE, 
                                            (y + self.y_offset) * self.ELEVATION_SCALE)
        secondary = self.elevation_noise.noise2((x + self.x_offset) * self.ELEVATION_SCALE * 2, 
                                              (y + self.y_offset) * self.ELEVATION_SCALE * 2) * 0.5
        return (primary + secondary) / 1.5

    def _get_moisture(self, x: int, y: int) -> float:
        """Generate moisture value for coordinates"""
        # Add offsets and multiple noise layers for more variation
        primary = self.moisture_noise.noise2((x + self.x_offset) * self.MOISTURE_SCALE,
                                           (y + self.y_offset) * self.MOISTURE_SCALE)
        secondary = self.moisture_noise.noise2((x + self.x_offset) * self.MOISTURE_SCALE * 2,
                                             (y + self.y_offset) * self.MOISTURE_SCALE * 2) * 0.5
        return (primary + secondary) / 1.5

    def _determine_biome(self, x: int, y: int) -> BiomeType:
        """Determine biome based on elevation and moisture with some randomization"""
        elevation = self._get_elevation(x, y)
        moisture = self._get_moisture(x, y)
        
        # Add slight random variation
        elevation += random.uniform(-0.1, 0.1)
        moisture += random.uniform(-0.1, 0.1)
        
        # Convert noise values to categories with more granular thresholds
        if elevation > 0.4:
            elev_category = 'high'
        elif elevation > 0.1:
            elev_category = 'medium'
        elif elevation > -0.2:
            elev_category = 'medium' if random.random() > 0.3 else 'low'
        else:
            elev_category = 'low'
            
        if moisture > 0.3:
            moist_category = 'wet'
        elif moisture > 0:
            moist_category = 'medium'
        elif moisture > -0.3:
            moist_category = 'medium' if random.random() > 0.3 else 'dry'
        else:
            moist_category = 'dry'
        
        return self.BIOME_MATRIX[elev_category][moist_category]

    def _generate_features(self, biome: BiomeType) -> list:
        """Generate list of features for the location based on biome"""
        features = []
        feature_chance = random.random()
        
        biome_features = {
            BiomeType.FOREST: [
                {"type": "tree", "variant": random.choice(["oak", "pine", "birch", "maple"])},
                {"type": "bush", "variant": random.choice(["berry", "flower", "thorny"])},
                {"type": "mushroom", "variant": random.choice(["red", "brown", "spotted"])}
            ],
            BiomeType.MOUNTAIN: [
                {"type": "rock", "variant": random.choice(["boulder", "cliff", "cave"])},
                {"type": "mineral", "variant": random.choice(["crystal", "ore", "gems"])}
            ],
            BiomeType.PLAINS: [
                {"type": "grass", "variant": random.choice(["tall", "flowering", "wild"])},
                {"type": "creature", "variant": random.choice(["rabbit", "deer", "bird"])}
            ],
            BiomeType.DESERT: [
                {"type": "cactus", "variant": random.choice(["barrel", "saguaro", "prickly"])},
                {"type": "dune", "variant": random.choice(["rolling", "steep", "windswept"])}
            ],
            BiomeType.SWAMP: [
                {"type": "water", "variant": random.choice(["pool", "marsh", "bog"])},
                {"type": "vegetation", "variant": random.choice(["vine", "moss", "reed"])}
            ],
            BiomeType.TUNDRA: [
                {"type": "ice", "variant": random.choice(["formation", "sheet", "crystal"])},
                {"type": "rock", "variant": random.choice(["frozen", "snow-covered", "weathered"])}
            ]
        }
        
        # 60% chance of having 1 feature, 30% chance of 2 features
        if feature_chance < 0.6:
            features.append(random.choice(biome_features.get(biome, [])))
        elif feature_chance < 0.9:
            features.extend(random.sample(biome_features.get(biome, []), 2))
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
