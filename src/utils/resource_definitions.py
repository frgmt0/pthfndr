from typing import Dict, Any

RESOURCE_DEFINITIONS = {
    "herbs": {
        "types": ["healing", "magical", "poisonous", "aromatic", "medicinal"],
        "interactions": {
            "gather": "You carefully gather some {variant} herbs.",
            "examine": "You find a patch of {variant} herbs growing here.",
            "smell": "The {variant} herbs give off a {quality} aroma."
        },
        "qualities": ["sweet", "pungent", "earthy", "mysterious", "fresh"]
    },
    "wood": {
        "types": ["oak", "pine", "birch", "ancient", "magical"],
        "interactions": {
            "gather": "You collect some {variant} wood.",
            "examine": "You find some {quality} {variant} wood.",
            "chop": "You begin chopping the {variant} wood."
        },
        "qualities": ["sturdy", "weathered", "fresh", "rare", "common"]
    },
    "ore": {
        "types": ["iron", "gold", "silver", "copper", "mysterious"],
        "interactions": {
            "mine": "You carefully mine some {variant} ore.",
            "examine": "You discover a vein of {variant} ore.",
            "analyze": "The {variant} ore appears to be {quality}."
        },
        "qualities": ["pure", "mixed", "rich", "poor", "exceptional"]
    }
}

def get_resource_definition(resource_type: str) -> Dict[str, Any]:
    """Get the definition for a specific resource"""
    return RESOURCE_DEFINITIONS.get(resource_type.lower(), {})

def get_resource_interaction(resource_type: str, interaction: str, variant: str = None, quality: str = None) -> str:
    """Get the interaction text for a resource, with optional variant and quality"""
    resource = get_resource_definition(resource_type)
    if not resource or interaction not in resource.get("interactions", {}):
        return "You cannot interact with this resource that way."
        
    interaction_text = resource["interactions"][interaction]
    
    if variant and "{variant}" in interaction_text:
        interaction_text = interaction_text.replace("{variant}", variant)
    if quality and "{quality}" in interaction_text:
        interaction_text = interaction_text.replace("{quality}", quality)
        
    return interaction_text
