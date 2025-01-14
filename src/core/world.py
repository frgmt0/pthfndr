from opensimplex import OpenSimplex
from src.models.base import BiomeType, Location
from src.core.weather import WeatherSystem, WeatherType
import random
from typing import Tuple, Dict, Any

class WorldGenerator:
    def __init__(self, seed: int = None):
        self.seed = seed or random.randint(0, 1000000)
        # Create two noise generators for more varied terrain
        self.elevation_noise = OpenSimplex(seed=self.seed)
        self.moisture_noise = OpenSimplex(seed=self.seed + 1)
        
        # Configure multi-layered noise parameters
        self.ELEVATION_SCALES = [0.02, 0.04, 0.08]  # Multiple scales for varied terrain
        self.MOISTURE_SCALES = [0.015, 0.03, 0.06]  # Multiple scales for varied moisture
        self.WEIGHTS = [0.5, 0.3, 0.2]  # Weights for each scale layer
        
        # Add some random offset to prevent grid-like patterns
        self.x_offset = random.uniform(-2000, 2000)
        self.y_offset = random.uniform(-2000, 2000)
        
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
        """Generate elevation value using multiple noise layers"""
        elevation = 0
        for scale, weight in zip(self.ELEVATION_SCALES, self.WEIGHTS):
            elevation += weight * self.elevation_noise.noise2(
                (x + self.x_offset) * scale,
                (y + self.y_offset) * scale
            )
        # Normalize to [-1, 1] range
        return elevation / sum(self.WEIGHTS)

    def _get_moisture(self, x: int, y: int) -> float:
        """Generate moisture value using multiple noise layers"""
        moisture = 0
        for scale, weight in zip(self.MOISTURE_SCALES, self.WEIGHTS):
            moisture += weight * self.moisture_noise.noise2(
                (x + self.x_offset) * scale,
                (y + self.y_offset) * scale
            )
        # Add some local variation
        local_variation = random.uniform(-0.1, 0.1)
        return (moisture / sum(self.WEIGHTS)) + local_variation

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
                {"type": "tree", "variant": random.choice(["oak", "pine", "birch", "maple", "ancient", "magical", "hollow"])},
                {"type": "bush", "variant": random.choice(["berry", "flower", "thorny", "healing", "poisonous", "glowing"])},
                {"type": "mushroom", "variant": random.choice(["red", "brown", "spotted", "giant", "luminous", "medicinal"])},
                {"type": "landmark", "variant": random.choice(["shrine", "statue", "ruins", "camp", "cave"])},
                {"type": "creature_nest", "variant": random.choice(["bird", "squirrel", "fox", "owl", "fairy"])},
                {"type": "resource", "variant": random.choice(["herbs", "fruits", "wood", "flowers", "honey"])}
            ],
            BiomeType.MOUNTAIN: [
                {"type": "rock", "variant": random.choice(["boulder", "cliff", "cave", "arch", "peak", "crystal"])},
                {"type": "mineral", "variant": random.choice(["crystal", "ore", "gems", "gold", "silver", "diamond"])},
                {"type": "landmark", "variant": random.choice(["shrine", "mine", "bridge", "watchtower", "tomb"])},
                {"type": "creature_nest", "variant": random.choice(["eagle", "goat", "dragon", "griffin", "yeti"])},
                {"type": "weather", "variant": random.choice(["mist", "storm", "snow", "wind", "clear"])},
                {"type": "path", "variant": random.choice(["steep", "winding", "dangerous", "hidden", "ancient"])}
            ],
            BiomeType.PLAINS: [
                {"type": "grass", "variant": random.choice(["tall", "flowering", "wild", "golden", "magical", "whispering"])},
                {"type": "creature", "variant": random.choice(["rabbit", "deer", "bird", "unicorn", "wolf", "fairy"])},
                {"type": "landmark", "variant": random.choice(["well", "stone_circle", "camp", "village", "tower"])},
                {"type": "water", "variant": random.choice(["stream", "pond", "spring", "oasis", "waterfall"])},
                {"type": "resource", "variant": random.choice(["herbs", "berries", "flowers", "grain", "cotton"])},
                {"type": "structure", "variant": random.choice(["fence", "bridge", "signpost", "shelter", "ruins"])}
            ],
            BiomeType.DESERT: [
                {"type": "cactus", "variant": random.choice(["barrel", "saguaro", "prickly", "flowering", "giant", "rare"])},
                {"type": "dune", "variant": random.choice(["rolling", "steep", "windswept", "shifting", "massive", "golden"])},
                {"type": "landmark", "variant": random.choice(["oasis", "ruins", "pyramid", "temple", "mirage"])},
                {"type": "creature_nest", "variant": random.choice(["scorpion", "snake", "lizard", "phoenix", "djinn"])},
                {"type": "resource", "variant": random.choice(["water", "dates", "minerals", "herbs", "crystals"])},
                {"type": "structure", "variant": random.choice(["well", "shelter", "camp", "tomb", "trading_post"])}
            ],
            BiomeType.SWAMP: [
                {"type": "water", "variant": random.choice(["pool", "marsh", "bog", "river", "quicksand", "mystic_pool"])},
                {"type": "vegetation", "variant": random.choice(["vine", "moss", "reed", "mangrove", "mushroom", "willow"])},
                {"type": "landmark", "variant": random.choice(["hut", "ruins", "altar", "bridge", "statue"])},
                {"type": "creature_nest", "variant": random.choice(["frog", "snake", "bird", "witch", "spirit"])},
                {"type": "resource", "variant": random.choice(["herbs", "roots", "fish", "magic_essence", "poison"])},
                {"type": "atmosphere", "variant": random.choice(["fog", "mist", "glow", "darkness", "whispers"])}
            ],
            BiomeType.TUNDRA: [
                {"type": "ice", "variant": random.choice(["formation", "sheet", "crystal", "cave", "bridge", "sculpture"])},
                {"type": "rock", "variant": random.choice(["frozen", "snow-covered", "weathered", "crystal", "magical"])},
                {"type": "landmark", "variant": random.choice(["cave", "shrine", "monolith", "settlement", "beacon"])},
                {"type": "creature_nest", "variant": random.choice(["penguin", "seal", "bear", "wolf", "frost_giant"])},
                {"type": "weather", "variant": random.choice(["blizzard", "aurora", "clear", "storm", "whiteout"])},
                {"type": "resource", "variant": random.choice(["ice_crystal", "fur", "fish", "magic_ice", "minerals"])}
            ]
        }
        
        # Enhanced feature generation:
        # 40% chance: 1 feature
        # 30% chance: 2 features
        # 20% chance: 3 features
        # 10% chance: 4 features
        if feature_chance < 0.4:
            features.append(random.choice(biome_features.get(biome, [])))
        elif feature_chance < 0.7:
            features.extend(random.sample(biome_features.get(biome, []), 2))
        elif feature_chance < 0.9:
            features.extend(random.sample(biome_features.get(biome, []), 3))
        else:
            features.extend(random.sample(biome_features.get(biome, []), 4))
        return features

    def _generate_description(self, biome: BiomeType, features: list, weather: WeatherType) -> str:
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

    def generate_location(self, x: int, y: int) -> Tuple[BiomeType, list, str, str]:
        """Generate a complete location at the given coordinates"""
        biome = self._determine_biome(x, y)
        elevation = self._get_elevation(x, y)
        weather = WeatherSystem.get_weather(biome, elevation)
        features = self._generate_features(biome)
        description = self._generate_description(biome, features, weather)
        
        # Add weather description
        weather_descriptions = {
            WeatherType.CLEAR: "The sky is clear and bright.",
            WeatherType.CLOUDY: "Gray clouds drift overhead.",
            WeatherType.RAIN: "A steady rain falls from above.",
            WeatherType.STORM: "Thunder rumbles as storm clouds loom.",
            WeatherType.SNOW: "Snowflakes drift gently from the sky.",
            WeatherType.BLIZZARD: "Howling winds drive snow through the air.",
            WeatherType.SANDSTORM: "Sand whips through the air in stinging clouds.",
            WeatherType.FOG: "A thick fog limits visibility.",
            WeatherType.MISTY: "A light mist hangs in the air."
        }
        
        description += f" {weather_descriptions[weather]}"
        
        return biome, features, description, weather
