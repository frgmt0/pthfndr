import asyncio
from tortoise import Tortoise
import os
from dotenv import load_dotenv
from src.core.game_manager import GameManager
from colorama import init, Fore, Style

load_dotenv()
init(autoreset=True)  # Initialize colorama

async def init_db():
    """Initialize database connection"""
    await Tortoise.init(
        db_url=os.getenv('DATABASE_URL'),
        modules={'models': ['src.models.base']}
    )
    await Tortoise.generate_schemas()

async def test_game_flow():
    """Test the game flow with some dummy data"""
    # Create game manager with fixed seed for reproducible results
    game_manager = GameManager(seed=12345)
    
    # Start new game
    print(f"{Fore.GREEN}Starting new game...{Style.RESET_ALL}")
    game_state = await game_manager.new_game()
    print(f"Game started with ID: {game_state.id}")
    
    # Get initial location
    location = await game_manager.get_current_location()
    print(f"\n{Fore.CYAN}Current Location:{Style.RESET_ALL}")
    print(f"Position: ({location.x}, {location.y})")
    print(f"Biome: {location.biome_type}")
    print(f"Description: {location.description}")
    
    # Get available actions
    actions = await game_manager.get_available_actions()
    print(f"\n{Fore.YELLOW}Available Actions:{Style.RESET_ALL}")
    for action in actions:
        print(f"- {action['type']}: {action}")
    
    # Test movement in each direction
    directions = ["north", "east", "south", "west"]
    for direction in directions:
        print(f"\n{Fore.GREEN}Moving {direction}...{Style.RESET_ALL}")
        result, updates = await game_manager.process_action("move", {
            "direction": direction,
            "distance": 100
        })
        print(result)
        print(f"State updates: {updates}")
        
        # Get new location details
        location = await game_manager.get_current_location()
        print(f"New biome: {location.biome_type}")
        
        # Test feature interaction if any
        if location.features:
            feature = location.features[0]
            print(f"\n{Fore.MAGENTA}Testing interaction...{Style.RESET_ALL}")
            result, updates = await game_manager.process_action("interact", {
                "target": feature["type"],
                "variant": feature["variant"]
            })
            print(result)
    
    # Save game state
    await game_manager.save_game()
    print(f"\n{Fore.GREEN}Game state saved!{Style.RESET_ALL}")

async def main():
    # Initialize database
    await init_db()
    
    try:
        # Run test flow
        await test_game_flow()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    finally:
        # Cleanup
        await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(main())
