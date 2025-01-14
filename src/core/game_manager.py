from typing import List, Dict, Any, Optional, Tuple
from src.models.base import GameState, Location, BiomeType, Item
from src.core.world import WorldGenerator
from src.core.weather import WeatherSystem
from tortoise.exceptions import DoesNotExist
import random

class GameManager:
    def __init__(self, seed: Optional[int] = None):
        """Initialize the game manager with optional seed"""
        self.seed = seed or random.randint(0, 1000000)
        self.world_generator = WorldGenerator(seed=self.seed)
        self.current_game_state: Optional[GameState] = None

    async def new_game(self) -> GameState:
        """Create a new game state"""
        self.current_game_state = await GameState.create(
            seed=self.seed,
            current_position={"x": 0, "y": 0},
            current_biome=BiomeType.PLAINS,  # Starting biome
            inventory={},
            health=100,
            weather=WeatherSystem.get_weather(BiomeType.PLAINS, 0)
        )
        return self.current_game_state

    async def load_game(self, game_state_id: int) -> GameState:
        """Load an existing game state"""
        try:
            self.current_game_state = await GameState.get(id=game_state_id)
            return self.current_game_state
        except DoesNotExist:
            raise ValueError(f"No game state found with id {game_state_id}")

    async def get_current_location(self) -> Location:
        """Get or generate the current location"""
        if not self.current_game_state:
            raise ValueError("No active game state")
        
        pos = self.current_game_state.current_position
        location = await Location.get_or_none(x=pos["x"], y=pos["y"])
        
        if not location:
            biome, features, description, weather = self.world_generator.generate_location(
                pos["x"], pos["y"]
            )
            location = await Location.create(
                x=pos["x"],
                y=pos["y"],
                biome_type=biome,
                features=features,
                description=description,
                weather=weather
            )
        
        return location

    async def get_inventory(self) -> List[Dict[str, Any]]:
        """Get current inventory items"""
        if not self.current_game_state:
            raise ValueError("No active game state")
        
        items = await self.current_game_state.items.all()
        return [{"name": item.name, "type": item.item_type, "description": item.description} 
                for item in items]

    async def add_item(self, name: str, item_type: str, description: str, properties: dict = None) -> str:
        """Add an item to inventory"""
        if not self.current_game_state:
            raise ValueError("No active game state")
            
        await Item.create(
            name=name,
            item_type=item_type,
            description=description,
            properties=properties or {},
            game_state=self.current_game_state
        )
        return f"Added {name} to inventory"

    async def drop_item(self, item_name: str) -> str:
        """Remove an item from inventory"""
        if not self.current_game_state:
            raise ValueError("No active game state")
            
        item = await Item.get_or_none(
            game_state=self.current_game_state,
            name=item_name
        )
        if item:
            await item.delete()
            return f"Dropped {item_name}"
        return f"No item named {item_name} in inventory"

    async def get_available_actions(self) -> List[Dict[str, Any]]:
        """Get list of available actions at current location"""
        if not self.current_game_state:
            raise ValueError("No active game state")
            
        location = await self.get_current_location()
        actions = []
        
        # Movement actions
        for direction in ["north", "south", "east", "west"]:
            actions.append({
                "type": "move",
                "direction": direction,
                "distances": [50, 100, 150]
            })
        
        # Feature interaction actions
        for feature in location.features:
            actions.append({
                "type": "interact",
                "target": feature["type"],
                "variant": feature["variant"]
            })
            
        return actions

    async def get_best_action(self) -> Dict[str, Any]:
        """Use MCTS to select the best action"""
        from src.core.mcts_manager import MCTSManager
        mcts = MCTSManager(self)
        return await mcts.select_action(self.current_game_state)

    async def process_action(self, action_type: str, params: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Process a player action and return the result"""
        if not self.current_game_state:
            raise ValueError("No active game state")
            
        result_description = ""
        state_updates = {}
        
        if action_type == "move":
            # Handle movement
            direction = params.get("direction")
            distance = params.get("distance", 100)
            
            # Calculate new position
            current_pos = self.current_game_state.current_position
            new_pos = current_pos.copy()
            
            if direction == "north":
                new_pos["y"] += 1
            elif direction == "south":
                new_pos["y"] -= 1
            elif direction == "east":
                new_pos["x"] += 1
            elif direction == "west":
                new_pos["x"] -= 1
                
            # Generate or get new location
            self.current_game_state.current_position = new_pos
            new_location = await self.get_current_location()
            
            # Update game state
            self.current_game_state.current_biome = new_location.biome_type
            await self.current_game_state.save()
            
            result_description = f"You travel {direction} for {distance} yards.\n{new_location.description}"
            state_updates = {"position": new_pos, "biome": new_location.biome_type}
            
        elif action_type == "interact":
            # Handle interaction with features
            target = params.get("target")
            variant = params.get("variant")
            
            location = await self.get_current_location()
            for feature in location.features:
                if feature["type"] == target and feature["variant"] == variant:
                    result_description = f"You interact with the {variant} {target}."
                    # Add specific interaction logic here
                    break
                    
        return result_description, state_updates

    async def save_game(self) -> None:
        """Save current game state"""
        if self.current_game_state:
            await self.current_game_state.save()
