import random
import numpy as np

class SOMPiBrain(object): # Simple Q-Learning agent

    def __init__(self, state_num, action_num, q_table=False, alpha=0.1, gamma=0.7, epsilon=0.1):
        self.alpha = alpha      # Learning speed-quality relation (Recommended 0.1)
                                    # Close to 1: Fast learning (adaptation), low quality
                                    # Close to 0: Low learning, high quality
        
        self.gamma = gamma      # Importance of future/immediate rewards (Recommended 0.9)
                                    # Close to 1: Prioritizes future rewards
                                    # Close to 0: Prioritizes immediate rewards

        self.epsilon = epsilon  # Exploration rate: (Recommended 0.9 and reduce progressively)
                                    # Probability of picking a random action instead of an intelligent

        self.action_num = action_num # Qty of possible actions
        
        # If any table available, use existing q_table
        if isinstance(q_table, np.ndarray) and q_table.size > 0:
            self.q_table = q_table
        else:
            self.q_table = np.zeros([state_num, action_num])

    def get_action(self, state, explore=True):
        """ Decides whether random or intelligent action and executes it """
        if explore and (random.uniform(0, 1) < self.epsilon):
            return random.randint(0, self.action_num - 1) # Random action
        else:
            return np.argmax(self.q_table[state]) # Most currently adequate action
            # argmax returns the index of the max value in the array

    def reward_action(self, state, action, next_state, reward): #
        """ Updates Qtable after recieving reward for taking an action from 'state' to 'next_sate' """
        old_value = self.q_table[state, action] # Rating action for old state
        next_max = np.max(self.q_table[next_state])
        # Fórmula Q-learning:
        # Q(s,a) ← Q(s,a) + α [r + γ max_a' Q(s',a') - Q(s,a)]
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[state, action] = new_value
        return next_state