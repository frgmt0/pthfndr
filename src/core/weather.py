from enum import Enum
from typing import Dict, Optional
import random
from src.models.base import BiomeType

class WeatherType(str, Enum):
    CLEAR = "clear"
    CLOUDY = "cloudy"
    RAIN = "rain"
    STORM = "storm"
    SNOW = "snow"
    BLIZZARD = "blizzard"
    SANDSTORM = "sandstorm"
    FOG = "fog"
    MISTY = "misty"

class WeatherSystem:
    # Weather probabilities per biome
    BIOME_WEATHER = {
        BiomeType.FOREST: {
            WeatherType.CLEAR: 0.3,
            WeatherType.CLOUDY: 0.3,
            WeatherType.RAIN: 0.2,
            WeatherType.STORM: 0.1,
            WeatherType.FOG: 0.1
        },
        BiomeType.PLAINS: {
            WeatherType.CLEAR: 0.4,
            WeatherType.CLOUDY: 0.3,
            WeatherType.RAIN: 0.2,
            WeatherType.STORM: 0.1
        },
        BiomeType.MOUNTAIN: {
            WeatherType.CLEAR: 0.2,
            WeatherType.CLOUDY: 0.2,
            WeatherType.SNOW: 0.3,
            WeatherType.BLIZZARD: 0.2,
            WeatherType.FOG: 0.1
        },
        BiomeType.DESERT: {
            WeatherType.CLEAR: 0.7,
            WeatherType.CLOUDY: 0.1,
            WeatherType.SANDSTORM: 0.2
        },
        BiomeType.SWAMP: {
            WeatherType.CLEAR: 0.2,
            WeatherType.CLOUDY: 0.3,
            WeatherType.RAIN: 0.2,
            WeatherType.FOG: 0.3
        },
        BiomeType.TUNDRA: {
            WeatherType.CLEAR: 0.2,
            WeatherType.CLOUDY: 0.2,
            WeatherType.SNOW: 0.3,
            WeatherType.BLIZZARD: 0.3
        }
    }

    @classmethod
    def get_weather(cls, biome: BiomeType, elevation: float = 0) -> WeatherType:
        """Generate weather appropriate for the biome and elevation"""
        weather_probs = cls.BIOME_WEATHER[biome].copy()
        
        # Adjust probabilities based on elevation
        if elevation > 0.5:  # High elevation
            # Increase chances of clear weather and snow
            weather_probs[WeatherType.CLEAR] = weather_probs.get(WeatherType.CLEAR, 0) * 1.2
            weather_probs[WeatherType.SNOW] = weather_probs.get(WeatherType.SNOW, 0) * 1.3
        elif elevation < -0.5:  # Low elevation
            # Increase chances of fog and rain
            weather_probs[WeatherType.FOG] = weather_probs.get(WeatherType.FOG, 0) * 1.3
            weather_probs[WeatherType.RAIN] = weather_probs.get(WeatherType.RAIN, 0) * 1.2

        # Normalize probabilities
        total = sum(weather_probs.values())
        normalized_probs = {k: v/total for k, v in weather_probs.items()}

        # Select weather based on probabilities
        rand = random.random()
        cumulative = 0
        for weather, prob in normalized_probs.items():
            cumulative += prob
            if rand <= cumulative:
                return weather
        
        return WeatherType.CLEAR  # Fallback
