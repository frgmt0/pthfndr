# Basics of Pathfinder

## Introduction
Pathfinder is a text-based adventure game where you explore an infinite, procedurally generated world. Each playthrough is unique, with different biomes, weather patterns, and encounters waiting to be discovered.

## Getting Started

### Starting the Game
To start the game, run:
```bash
uv run python main.py
```
or just run `python main.py`

The game will generate a new world and place you at the starting position (0,0) in the Plains biome.

### Basic Commands
- `move <direction> [distance]` - Move in a direction (north, south, east, west)
  Example: `move north 100`
  
- `interact <target> <variant>` - Interact with features in your environment
  Example: `interact tree ancient`
  
- `inventory` - Check your current inventory
- `take <item>` - Pick up an item
- `drop <item>` - Drop an item
- `quit` - Save and exit the game

## World Navigation

### Biomes
The world contains six distinct biomes:
- Forest (FRST) - Dense woodland areas with abundant resources
- Plains (PLNS) - Open grasslands with good visibility
- Mountain (MNTN) - Challenging terrain with valuable minerals
- Desert (DSRT) - Harsh environments with unique resources
- Swamp (SWMP) - Wet, mysterious areas with rare plants
- Tundra (TNDR) - Cold regions with unique challenges

### Weather System
Each biome has its own weather patterns that can affect gameplay:
- Clear
- Cloudy
- Rain
- Storm
- Snow
- Blizzard
- Sandstorm
- Fog
- Misty

## Interactions

### Features
Each location may contain various features you can interact with:
- Natural features (trees, rocks, water)
- Creatures (fish, animals)
- Structures (bridges, shrines, camps)
- Resources (herbs, wood, ore)

### Basic Interaction Flow
1. When you enter a location, the game describes what you see
2. Use `interact` to engage with features
3. Follow the prompts to perform specific actions
4. Use `leave` to end the interaction

Example:
```
> interact tree ancient
Interacting with ancient tree
Available actions:
- examine
- climb
- rest
- leave
```

## Inventory System

### Items
Items are categorized into different types:
- Weapons
- Armor
- Potions
- Tools
- Treasure
- Keys

### Managing Items
- Check your inventory regularly
- Use `take` to collect items you find
- Use `drop` to discard unwanted items
- Some items have special properties or uses

## Tips for New Players

1. **Explore Carefully**
   - Pay attention to biome descriptions
   - Note interesting features for later return
   - Watch the weather conditions

2. **Resource Management**
   - Collect useful resources when found
   - Don't overload your inventory
   - Save valuable items for later use

3. **Interaction Strategy**
   - Always examine new features
   - Try different interaction options
   - Remember successful interactions

4. **Navigation**
   - Keep track of your position
   - Use landmarks as reference points
   - Explore systematically

## Advanced Features

### Multi-Stage Interactions
Some features require multiple steps to fully interact with:
1. Initial examination
2. Discovering requirements
3. Meeting conditions
4. Completing interaction

### Success Chances
Certain interactions have varying chances of success based on:
- Player skills
- Item requirements
- Environmental conditions

## Saving and Loading

- The game automatically saves your progress
- Your position, inventory, and game state are preserved
- Resume your adventure any time by launching the game

## Need Help?

If you encounter any issues or have questions:
1. Check this documentation
2. Look for similar issues on GitHub
3. Create a new issue if needed

Happy adventuring!