import numpy as np
import random
import tensorflow as tf

class LearningAgent:
    def __init__(self, player):
        self.player = player
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 1.0

    def choose_action(self, state, valid_moves):
        #Using Epsilon greedy policy
        valid_move_list = list(valid_moves.keys())
        if random.uniform(0,1) < self.exploration_rate:
            return random.choice(valid_move_list)
        else:
            state_q_values = self.q_table.get(state,{})
            return max(valid_move_list, key = lambda move: state_q_values.get(move,0))
        
    def update_q_vales(self, state, action, reward, next_state):
        best_next_action = max(self.q_table.get(next_state, {}).values(), default = 0)
        self.q_table[state][action] = (1 - self.learning_rate) * self.q_table.get(state, {}).get(action, 0) + self.learning_rate * (reward + self.discount_factor * best_next_action)

    def calculate_reward(self, game, action, player, opponent):
        if action not in player.availablemove:
            return -1

        if game.game_over():
            if game.winner(player) == player:
                return 10000
            elif game.winner(player) is None:
                return 0
            else:
                return -100
            
        else:
            return player.score - opponent.score
        