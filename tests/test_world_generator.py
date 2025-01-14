import pytest
from src.core.world import WorldGenerator
from src.models.base import BiomeType
from src.core.weather import WeatherType

@pytest.fixture
def world_generator():
    return WorldGenerator(seed=12345)

def test_elevation_generation(world_generator):
    """Test that elevation values are within expected range"""
    elevation = world_generator._get_elevation(0, 0)
    assert -1 <= elevation <= 1

def test_moisture_generation(world_generator):
    """Test that moisture values are within expected range"""
    moisture = world_generator._get_moisture(0, 0)
    assert -1 <= moisture <= 1

def test_biome_determination(world_generator):
    """Test that biome determination returns valid biome types"""
    biome = world_generator._determine_biome(0, 0)
    assert isinstance(biome, BiomeType)
    assert biome in BiomeType.__members__.values()

def test_feature_generation(world_generator):
    """Test that features are generated appropriately for each biome"""
    for biome in BiomeType:
        features = world_generator._generate_features(biome)
        assert isinstance(features, list)
        assert len(features) > 0
        for feature in features:
            assert isinstance(feature, dict)
            assert "type" in feature
            assert "variant" in feature

def test_location_generation(world_generator):
    """Test complete location generation"""
    biome, features, description, weather = world_generator.generate_location(0, 0)
    
    assert isinstance(biome, BiomeType)
    assert isinstance(features, list)
    assert isinstance(description, str)
    assert isinstance(weather, WeatherType)
    assert len(description) > 0

def test_deterministic_generation(world_generator):
    """Test that the same seed produces the same results"""
    gen1 = WorldGenerator(seed=12345)
    gen2 = WorldGenerator(seed=12345)
    
    loc1 = gen1.generate_location(0, 0)
    loc2 = gen2.generate_location(0, 0)
    
    assert loc1 == loc2
