import pytest
from src.core.game_manager import GameManager
from src.models.base import GameState, Location, BiomeType
from tortoise import Tortoise
import os

@pytest.fixture(autouse=True)
async def setup_db():
    """Setup test database before each test"""
    await Tortoise.init(
        db_url='sqlite://:memory:',
        modules={'models': ['src.models.base']}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

@pytest.fixture
async def game_manager():
    return GameManager(seed=12345)

@pytest.mark.asyncio
async def test_new_game(game_manager):
    """Test creating a new game"""
    game_state = await game_manager.new_game()
    
    assert isinstance(game_state, GameState)
    assert game_state.seed == 12345
    assert game_state.current_position == {"x": 0, "y": 0}
    assert game_state.health == 100
    assert isinstance(game_state.current_biome, BiomeType)

@pytest.mark.asyncio
async def test_get_current_location(game_manager):
    """Test getting current location"""
    await game_manager.new_game()
    location = await game_manager.get_current_location()
    
    assert isinstance(location, Location)
    assert location.x == 0
    assert location.y == 0
    assert isinstance(location.biome_type, BiomeType)
    assert len(location.description) > 0
    assert isinstance(location.features, list)

@pytest.mark.asyncio
async def test_movement_action(game_manager):
    """Test moving to a new location"""
    await game_manager.new_game()
    
    result, updates = await game_manager.process_action("move", {
        "direction": "north",
        "distance": 100
    })
    
    assert isinstance(result, str)
    assert "north" in result.lower()
    assert "position" in updates
    assert updates["position"]["y"] == 1

@pytest.mark.asyncio
async def test_get_available_actions(game_manager):
    """Test getting available actions"""
    await game_manager.new_game()
    actions = await game_manager.get_available_actions()
    
    assert isinstance(actions, list)
    assert len(actions) > 0
    
    # Should always have movement actions
    movement_actions = [a for a in actions if a["type"] == "move"]
    assert len(movement_actions) == 4  # north, south, east, west

@pytest.mark.asyncio
async def test_save_and_load_game(game_manager):
    """Test saving and loading game state"""
    original_state = await game_manager.new_game()
    await game_manager.save_game()
    
    # Create new manager and load saved game
    new_manager = GameManager(seed=12345)
    loaded_state = await new_manager.load_game(original_state.id)
    
    assert loaded_state.id == original_state.id
    assert loaded_state.seed == original_state.seed
    assert loaded_state.current_position == original_state.current_position
