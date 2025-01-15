# Pathfinder (pthfndr)
A Procedurally Generated Text Adventure Engine

## Overview
Pathfinder is an advanced text adventure engine that creates infinite, procedurally generated worlds with diverse biomes and uses Monte Carlo Tree Search (MCTS) with PostgreSQL to learn from and enhance player experiences.

## Features
- Procedurally generated infinite world
- Dynamic biome system with unique features
- Weather system affecting gameplay
- Intelligent NPC interactions using MCTS
- Persistent world state
- Rich item and inventory system
- Complex interaction system

## Requirements
- Python 3.13+
- PostgreSQL
- Required Python packages listed in requirements.txt

## Installation
1. Clone the repository:
```bash
git clone https://github.com/frgmt0/pthfndr.git
cd pthfndr
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
Or use `uv`
```bash
uv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
Or use `uv`
```bash
uv pip install -r requirements.txt
```

4. Set up the database:
- Copy `.env.example` to `.env`
- Update DATABASE_URL with your PostgreSQL credentials

## Usage
Run the game:
```bash
python main.py
```

Basic commands:
- `move <direction> [distance]` - Move in a direction (north, south, east, west)
- `interact <target> <variant>` - Interact with features in the environment
- `inventory` - Check your inventory
- `take <item>` - Pick up an item
- `drop <item>` - Drop an item
- `quit` - Save and exit the game

## Development
See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines and how to contribute to the project.

## Documentation
- [Privacy Policy](PRIVACY.md)
- [Security](SECURITY.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Community Guidelines](COMMUNITY_GUIDELINES.md)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support
For support, please:
1. Check the [documentation](docs/)
2. Search existing [issues](https://github.com/yourusername/pthfndr/issues)
3. Create a new issue if needed

## Acknowledgments
- OpenSimplex for noise generation
- Tortoise ORM for database management
- The Python community for various tools and libraries
