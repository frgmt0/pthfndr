from typing import Dict, Any

STRUCTURE_DEFINITIONS = {
    "bridge": {
        "type": "crossing",
        "interactions": {
            "cross": "You carefully walk across the bridge, the structure holding firm beneath your feet.",
            "examine": "The bridge appears to be {variant}, spanning across the gap.",
            "test": "You test the bridge's stability - it seems {condition}."
        },
        "conditions": ["sturdy", "somewhat stable", "rickety", "dangerous"],
        "variants": ["wooden", "stone", "rope", "ancient stone", "magical"]
    },
    "shrine": {
        "type": "religious",
        "interactions": {
            "pray": "You kneel before the shrine and offer a quiet prayer.",
            "examine": "The {variant} shrine stands solemnly, radiating an ancient presence.",
            "meditate": "You spend some time in quiet meditation at the shrine."
        },
        "variants": ["stone", "wooden", "crystal", "ancient", "forgotten"]
    },
    "camp": {
        "type": "shelter",
        "interactions": {
            "rest": "You take a moment to rest at the camp.",
            "examine": "The {variant} camp shows signs of {condition}.",
            "search": "You search through the camp carefully."
        },
        "conditions": ["recent use", "abandonment", "active occupation", "disarray"],
        "variants": ["abandoned", "traveler's", "hunter's", "merchant's"]
    }
}

def get_structure_definition(structure_type: str) -> Dict[str, Any]:
    """Get the definition for a specific structure"""
    return STRUCTURE_DEFINITIONS.get(structure_type.lower(), {})

def get_structure_interaction(structure_type: str, interaction: str, variant: str = None, condition: str = None) -> str:
    """Get the interaction text for a structure, with optional variant and condition"""
    structure = get_structure_definition(structure_type)
    if not structure or interaction not in structure.get("interactions", {}):
        return "You cannot interact with this structure that way."
        
    interaction_text = structure["interactions"][interaction]
    
    if variant and "{variant}" in interaction_text:
        interaction_text = interaction_text.replace("{variant}", variant)
    if condition and "{condition}" in interaction_text:
        interaction_text = interaction_text.replace("{condition}", condition)
        
    return interaction_text
