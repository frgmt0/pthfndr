from typing import List, Dict, Any, Optional, Tuple
from src.models.base import GameState, Location, BiomeType, Item, ItemType
from src.core.world import WorldGenerator
from src.core.weather import WeatherSystem
from src.utils.items import generate_item_name, generate_item_description, get_item_properties
from src.utils.item_definitions import get_item_definition
from src.utils.structure_definitions import get_structure_interaction
from src.utils.resource_definitions import get_resource_interaction
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
        return [{"name": item.name, 
                "type": item.item_type, 
                "description": item.description,
                "properties": item.properties} 
                for item in items]

    async def add_item(self, item_name: str) -> str:
        """Add an item to inventory based on name"""
        if not self.current_game_state:
            raise ValueError("No active game state")

        # Get current location features to check if item exists
        location = await self.get_current_location()
        item_found = False
        item_type = ItemType.TREASURE  # Default type
        
        # First check if the item exists in definitions
        item_def = get_item_definition(item_name.title())  # Try with title case
        if not item_def:
            item_def = get_item_definition(item_name)  # Try exact match
            
        if not item_def:
            return f"Unknown item: {item_name}"

        # Then check if the item can be found in the current location
        for feature in location.features:
            if (item_name.lower() in feature["variant"].lower() or 
                item_name.lower() in feature["type"].lower() or
                feature["type"].lower() == "resource"):  # Special handling for resources
                item_found = True
                item_type = item_def.get("type", ItemType.TREASURE)
                break
        
        if not item_found:
            return f"There is no {item_name} here to take."
            
        location = await self.get_current_location()
        description = f"{item_def['description']} (Found in {location.biome_type.value})"
        properties = get_item_properties(item_name)

        await Item.create(
            name=item_name,
            item_type=item_type,
            description=description,
            properties=properties,
            game_state=self.current_game_state
        )
        return f"Added {item_name} to inventory"

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

    def __init__(self, seed: Optional[int] = None):
        """Initialize the game manager with optional seed"""
        self.seed = seed or random.randint(0, 1000000)
        self.world_generator = WorldGenerator(seed=self.seed)
        self.current_game_state: Optional[GameState] = None
        from src.core.interactions import InteractionManager
        self.interaction_manager = InteractionManager(self)

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
                    interaction_type = params.get("interaction", "examine")
                    
                    # Generate default interaction messages based on feature type
                    default_interactions = {
                        "fish": {
                            "examine": f"You watch the {variant} fish swimming.",
                            "catch": f"You try to catch the {variant} fish.",
                            "feed": f"You throw some food to the {variant} fish."
                        },
                        "creature": {
                            "examine": f"You observe the {variant} carefully.",
                            "follow": f"You attempt to follow the {variant}.",
                            "call": f"You try to call the {variant} over."
                        },
                        "water": {
                            "examine": f"You look at the {variant} water.",
                            "drink": f"You take a drink from the {variant} water.",
                            "swim": f"You wade into the {variant} water."
                        }
                    }
                    
                    # First try structure definitions
                    structure_interaction = get_structure_interaction(
                        target, 
                        interaction_type,
                        variant,
                        feature.get("condition")
                    )
                    if structure_interaction != "You cannot interact with this structure that way.":
                        result_description = structure_interaction
                        break
                    
                    # Then try resource definitions
                    resource_interaction = get_resource_interaction(
                        target,
                        interaction_type,
                        variant,
                        feature.get("quality")
                    )
                    if resource_interaction != "You cannot interact with this resource that way.":
                        result_description = resource_interaction
                        break
                    
                    # Finally try default interactions
                    if target in default_interactions:
                        result_description = default_interactions[target].get(
                            interaction_type,
                            f"You {interaction_type} the {variant} {target}."
                        )
                    else:
                        # Generic fallback
                        result_description = f"You {interaction_type} the {variant} {target}."
                    break
                    
        return result_description, state_updates

    async def save_game(self) -> None:
        """Save current game state"""
        if self.current_game_state:
            await self.current_game_state.save()
