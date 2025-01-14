from typing import List, Dict, Any, Optional, Tuple
import math
import random
from src.models.base import GameState, Location
from src.core.game_manager import GameManager

class MCTSManager:
    def __init__(self, game_manager: GameManager, exploration_constant: float = 1.414):
        self.game_manager = game_manager
        self.exploration_constant = exploration_constant
        self.visits: Dict[str, int] = {}  # State visit counts
        self.rewards: Dict[str, float] = {}  # State total rewards
        self.children: Dict[str, List[str]] = {}  # State -> possible next states
        
    def _get_state_hash(self, state: GameState) -> str:
        """Generate a unique hash for a game state"""
        return f"{state.current_position}_{state.current_biome}_{state.health}"
        
    def _get_ucb1_score(self, state_hash: str, parent_hash: str) -> float:
        """Calculate UCB1 score for state selection"""
        if state_hash not in self.visits:
            return float('inf')
            
        exploitation = self.rewards[state_hash] / self.visits[state_hash]
        exploration = self.exploration_constant * math.sqrt(
            math.log(self.visits[parent_hash]) / self.visits[state_hash]
        )
        return exploitation + exploration
        
    async def select_action(self, current_state: GameState) -> Dict[str, Any]:
        """Select the best action using MCTS"""
        for _ in range(100):  # Number of simulations
            await self._simulate(current_state)
            
        # Get available actions
        actions = await self.game_manager.get_available_actions()
        
        # Select best action based on visit counts
        state_hash = self._get_state_hash(current_state)
        best_action = None
        max_visits = -1
        
        for action in actions:
            next_state_hash = f"{state_hash}_{action['type']}_{action.get('direction', '')}"
            visits = self.visits.get(next_state_hash, 0)
            
            if visits > max_visits:
                max_visits = visits
                best_action = action
                
        return best_action
        
    async def _simulate(self, state: GameState) -> float:
        """Run a single MCTS simulation"""
        visited_states = []
        current_state = state
        depth = 0
        total_reward = 0
        
        # Selection and expansion
        while depth < 10:  # Max simulation depth
            state_hash = self._get_state_hash(current_state)
            visited_states.append(state_hash)
            
            if state_hash not in self.visits:
                self.visits[state_hash] = 0
                self.rewards[state_hash] = 0
                break
                
            # Get available actions
            actions = await self.game_manager.get_available_actions()
            
            # Select action using UCB1
            best_score = float('-inf')
            best_action = None
            
            for action in actions:
                next_hash = f"{state_hash}_{action['type']}_{action.get('direction', '')}"
                score = self._get_ucb1_score(next_hash, state_hash)
                
                if score > best_score:
                    best_score = score
                    best_action = action
            
            if not best_action:
                break
                
            # Execute action
            result, updates = await self.game_manager.process_action(
                best_action["type"], best_action
            )
            
            # Calculate reward based on action result
            reward = self._calculate_reward(result, updates)
            total_reward += reward
            
            depth += 1
            
        # Backpropagation
        for state_hash in visited_states:
            self.visits[state_hash] = self.visits.get(state_hash, 0) + 1
            self.rewards[state_hash] = self.rewards.get(state_hash, 0) + total_reward
            
        return total_reward
        
    def _calculate_reward(self, result: str, updates: Dict[str, Any]) -> float:
        """Calculate reward for an action result"""
        reward = 0
        
        # Reward for discovering new locations
        if "position" in updates:
            reward += 1.0
            
        # Reward for finding interesting features
        if "discovered_feature" in updates:
            reward += 2.0
            
        # Reward for maintaining health
        if "health" in updates:
            health_change = updates["health"] - self.game_manager.current_game_state.health
            reward += health_change * 0.1
            
        return reward
