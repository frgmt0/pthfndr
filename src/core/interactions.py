from typing import Dict, Any, Tuple, List
from src.utils.structure_definitions import get_structure_interaction
from src.utils.resource_definitions import get_resource_interaction
from colorama import Fore, Style

class InteractionManager:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.current_feature = None
        
    async def start_interaction(self, target: str, variant: str) -> str:
        """Start interaction mode with a specific feature"""
        location = await self.game_manager.get_current_location()
        for feature in location.features:
            if feature["type"] == target and feature["variant"] == variant:
                self.current_feature = feature
                return self._get_interaction_prompt()
        return "Cannot find that feature here."
        
    def _get_interaction_prompt(self) -> str:
        """Get the interaction prompt for the current feature"""
        if not self.current_feature:
            return "No active interaction."
            
        feature_type = self.current_feature["type"]
        variant = self.current_feature["variant"]
        
        # Get available interactions based on feature type
        if feature_type == "resource":
            # For resources, get interactions from resource definitions
            resource_def = get_resource_definition(variant)
            interactions = list(resource_def.get("interactions", {}).keys())
            if not interactions:
                interactions = ["examine"]
        else:
            # Default interaction options based on feature type
            default_interactions = {
                "fish": ["examine", "catch", "feed"],
                "creature": ["examine", "follow", "call"],
                "water": ["examine", "drink", "swim"],
                "tree": ["examine", "climb", "rest"],
                "rock": ["examine", "climb", "search"],
                "plant": ["examine", "harvest", "smell"]
            }
            interactions = default_interactions.get(feature_type, ["examine"])
        
        # Build prompt
        prompt = f"\n{Fore.CYAN}Interacting with {variant} {feature_type}{Style.RESET_ALL}\n"
        prompt += "Available actions:\n"
        for action in interactions:
            prompt += f"- {action}\n"
        prompt += "- leave (end interaction)\n"
        
        return prompt
        
    async def process_interaction(self, action: str) -> str:
        """Process an interaction command"""
        if not self.current_feature:
            return "No active interaction."
            
        if action == "leave":
            self.current_feature = None
            return "Ending interaction."
            
        feature_type = self.current_feature["type"]
        variant = self.current_feature["variant"]
        
        # For resources, handle differently
        if feature_type == "resource":
            resource_result = get_resource_interaction(
                variant,  # For resources, the variant is the resource type
                action,
                variant,
                self.current_feature.get("quality")
            )
            if resource_result != "You cannot interact with this resource that way.":
                return resource_result
        else:
            # Try structure interaction first
            structure_result = get_structure_interaction(
                feature_type,
                action,
                variant,
                self.current_feature.get("condition")
            )
            if structure_result != "You cannot interact with this structure that way.":
                return structure_result
            
        # Default interactions based on feature type
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
            },
            "tree": {
                "examine": f"You look at the {variant} tree.",
                "climb": f"You attempt to climb the {variant} tree.",
                "rest": f"You rest under the {variant} tree."
            },
            "rock": {
                "examine": f"You examine the {variant} rock.",
                "climb": f"You try to climb the {variant} rock.",
                "search": f"You search around the {variant} rock."
            },
            "plant": {
                "examine": f"You look at the {variant} plant.",
                "harvest": f"You try to harvest the {variant} plant.",
                "smell": f"You smell the {variant} plant."
            }
        }
        
        if feature_type in default_interactions:
            return default_interactions[feature_type].get(
                action,
                f"You {action} the {variant} {feature_type}."
            )
            
        return f"You {action} the {variant} {feature_type}."
