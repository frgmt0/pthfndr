import asyncio
from tortoise import Tortoise
import os
from dotenv import load_dotenv
from src.core.world import WorldGenerator
from src.models.base import GameState, Location

load_dotenv()

async def init_db():
    await Tortoise.init(
        db_url=os.getenv('DATABASE_URL'),
        modules={'models': ['src.models.base']}
    )
    await Tortoise.generate_schemas()

async def get_or_create_location(x: int, y: int, world_gen: WorldGenerator) -> Location:
    """Get existing location or generate a new one"""
    location = await Location.get_or_none(x=x, y=y)
    if not location:
        biome, features, description = world_gen.generate_location(x, y)
        location = await Location.create(
            x=x,
            y=y,
            biome_type=biome,
            features=features,
            description=description
        )
    return location

async def main():
    # Initialize database
    await init_db()
    
    # Create world generator
    world_gen = WorldGenerator(seed=12345)
    
    # Test: Generate and print some locations
    print("Generating test locations...")
    for x in range(-1, 2):
        for y in range(-1, 2):
            location = await get_or_create_location(x, y, world_gen)
            print(f"\nLocation ({x}, {y}):")
            print(f"Biome: {location.biome_type}")
            print(f"Description: {location.description}")
    
    # Cleanup
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(main())
