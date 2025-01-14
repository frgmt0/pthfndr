import asyncio
from tortoise import Tortoise
import os
from dotenv import load_dotenv

load_dotenv()

async def init_db():
    await Tortoise.init(
        db_url=os.getenv('DATABASE_URL'),
        modules={'models': ['src.models.base']}
    )
    await Tortoise.generate_schemas()

async def main():
    # Initialize database
    await init_db()
    
    # Game loop will go here
    
    # Cleanup
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(main())
