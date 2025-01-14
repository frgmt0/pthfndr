import asyncio
from tortoise import Tortoise
import os
from dotenv import load_dotenv
from src.core.game_manager import GameManager
from src.models.base import ItemType
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

async def play_game():
    """Main game loop with user input"""
    # Create game manager with random seed
    game_manager = GameManager()
    
    print(f"{Fore.GREEN}Welcome to Pathfinder!{Style.RESET_ALL}")
    print("Starting new game...")
    game_state = await game_manager.new_game()
    
    while True:
        # Display current location
        location = await game_manager.get_current_location()
        print(f"\n{Fore.CYAN}Current Location:{Style.RESET_ALL}")
        print(f"Position: ({location.x}, {location.y})")
        print(f"Biome: {location.biome_type}")
        print(f"Description: {location.description}")
        print(f"Weather: {location.weather}")
        
        # Display available actions
        actions = await game_manager.get_available_actions()
        print(f"\n{Fore.YELLOW}Available Actions:{Style.RESET_ALL}")
        for action in actions:
            if action["type"] == "move":
                print(f"- move {action['direction']} [distance]")
            elif action["type"] == "interact":
                print(f"- interact {action['target']} {action['variant']}")
        
        # Get user input
        try:
            command = input(f"\n{Fore.GREEN}What would you like to do? {Style.RESET_ALL}").lower().split()
            
            if not command:
                continue
                
            if command[0] == "quit":
                print("Saving game and exiting...")
                await game_manager.save_game()
                break
                
            if command[0] == "move" and len(command) >= 2:
                direction = command[1]
                distance = int(command[2]) if len(command) > 2 else 100
                
                if direction in ["north", "south", "east", "west"]:
                    result, updates = await game_manager.process_action("move", {
                        "direction": direction,
                        "distance": distance
                    })
                    print(f"\n{result}")
                else:
                    print("Invalid direction. Use: north, south, east, or west")
                    
            elif command[0] == "interact" and len(command) >= 3:
                target = command[1]
                variant = command[2]
                result, updates = await game_manager.process_action("interact", {
                    "target": target,
                    "variant": variant
                })
                print(f"\n{result}")
                
            elif command[0] == "inventory":
                items = await game_manager.get_inventory()
                if items:
                    print(f"\n{Fore.YELLOW}Inventory:{Style.RESET_ALL}")
                    for item in items:
                        print(f"- {Fore.CYAN}{item['name']}{Style.RESET_ALL}")
                        print(f"  Type: {item['type']}")
                        print(f"  Description: {item['description']}")
                        if item['properties']:
                            print(f"  Properties:")
                            for prop, value in item['properties'].items():
                                print(f"    {prop}: {value}")
                else:
                    print("\nInventory is empty")
                    
            elif command[0] == "take" and len(command) >= 2:
                item_name = " ".join(command[1:])
                result = await game_manager.add_item(item_name)
                print(f"\n{result}")
                
            elif command[0] == "drop" and len(command) >= 2:
                item_name = " ".join(command[1:])
                result = await game_manager.drop_item(item_name)
                print(f"\n{result}")
                
            else:
                print("Invalid command. Available commands:")
                print("- move <direction> [distance]")
                print("- interact <target> <variant>")
                print("- inventory")
                print("- take <item_name>")
                print("- drop <item_name>")
                print("- quit")
                
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

async def main():
    # Initialize database
    await init_db()
    
    try:
        # Start the game loop
        await play_game()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    finally:
        # Cleanup
        await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(main())
