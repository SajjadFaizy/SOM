from game_logic import Game
from q_brain import SOMPiBrain
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle, os


def heuristic_move(game):
    """
    Makes an easy move (heuristic):
    If any disks on first tower, take superior disk
    Depending on even or uneven, move to tower 1 or 2
    """
    if game.towers[0].size > 0:
        largest_disk = game.towers[0][-1]
        target = 2 if largest_disk % 2 == 0 else 1
        game.move_ring(0, target)


def save_Qtable(table, training_index=False): # qbrain.qtable
    """
        Save Pickle File
    """
    base_dir = os.path.dirname(os.path.abspath(__file__)) # Abs route current directory
    qtables_dir = os.path.join(base_dir, "Qtables") # Route to Qtables
    # Create filename
    if training_index:
        filename = os.path.join(qtables_dir, f"{training_index}.pkl")
    else:
        os.path.join(qtables_dir, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pkl")
    # Save file
    with open(filename, "wb") as file:
        pickle.dump(table, file)

    """
        Export Pickle to readable CSV or 
    """
    output_file = filename.replace(".pkl", ".csv")
    data = pd.read_pickle(filename)
    if isinstance(data, np.ndarray): # If numpy array
        df = pd.DataFrame(data) # Array to DataFrame
    else:
        df = data
    df.to_csv(output_file, index=False) # Save

    # print(f"Qtable saved as: {filename} and {output_file}")


def load_Qtable(filename):
    """
    Loads existing Qtable
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    qtables_dir = os.path.join(base_dir, "Qtables")  # Qtables directory
    filepath = os.path.join(qtables_dir, filename)   # File path

    if os.path.exists(filepath):
        with open(filepath, "rb") as file:
            q_table = pickle.load(file)
        # print(f"Qtable cargada desde: {filepath}")
        return q_table
    else:
        raise FileNotFoundError(f"El archivo '{filename}' no existe en {qtables_dir}")


def print_hist(moves, training_index):

    x_values = list(range(len(moves)))

    # Create plot
    plt.bar(x_values, moves)

    # Personalisation
    plt.xlabel(f"Episode {training_index}")
    plt.ylabel("Move Qty")
    # plt.title("Gráfico de barras")
    # plt.xticks(x_values)  # Mostrar todos los índices en el eje x

    plt.show()


def train_brain(training_index, num_disks, num_episodes, max_steps_per_episode, q_table, alpha, epsilon, gamma):
    
    state_num = 3 ** num_disks # Qty possible states
    actions = [(0,1), (0,2), (1,0), (1,2), (2,0), (2,1)] # Possible actions (source->target):
    action_num = len(actions) # Qty possible actions 
    total_moves_hist = []

    q_brain = SOMPiBrain(state_num, action_num, epsilon=epsilon, alpha=alpha, gamma=gamma, q_table=q_table) # Instance Agent

    for episode in range(num_episodes):
        game = Game(num_disks)
        state_index = game.get_state_index()
        total_moves = 0
        max_disks_on_tower_3 = 0

        # Hacemos un primer movimiento heurístico
        heuristic_move(game)

        for _ in range(max_steps_per_episode):

            if game.is_solved():
                #print(f"\nEpisode {episode + 1} solved in {total_moves}")
                break

            # Get action from Q-Learning-Brain
            action = q_brain.get_action(state_index) # Choose action
            source, target = actions[action] # Extract source and target from chosen action
            
            # Execute action AND train model
            try: # to move ring
                game.move_ring(source, target)
                reward = 0.2
            except ValueError: # If chosen action is invalid move
                reward = -0.1

            # Reward solved game & penalty additional step
            reward += 7 * num_disks if game.is_solved() else -2

            # Reward for positioning more qty of disks on tower 3
            if len(game.towers[2]) > max_disks_on_tower_3:
                max_disks_on_tower_3 = len(game.towers[2])
                reward += 2

            # Redundance Penalty
            if np.any(game.history[:-1] == game.history[-1]): reward -= 10


            # Update Q-table
            next_state_index = game.get_state_index()
            q_brain.reward_action(state_index, action, next_state_index, reward)

            # Update Status
            state_index = next_state_index # Update state_index to search the next action in the next loop iteration (~l.131)
            total_moves += 1
    
        if not game.is_solved():
            print(f"\nEpisode {episode + 1}: Did not solve the game in {total_moves} moves.\n")
        else:
            total_moves_hist.append(total_moves)

    print(f"Training {training_index}: {sum(total_moves_hist) / len(total_moves_hist)}")
    save_Qtable(q_brain.q_table, training_index)
    print_hist(total_moves_hist, training_index)
    print("Training complete")

    return total_moves_hist



if __name__ == "__main__":

    num_disks = 3

    # Initial exploration
    """moves1 = train_brain(
        training_index = 1,
        num_disks = num_disks,
        num_episodes = 130,
        max_steps_per_episode = 1000,
        q_table = False,
        alpha=0.2,      # Learning speed-quality relation
        epsilon=0.9,    # Exploration rate
        gamma=0.8       # Importance of future rewards over immediate rewards
    )"""

    moves2 = train_brain(
        training_index = 2,
        num_disks = num_disks,
        num_episodes = 1000,
        max_steps_per_episode = 250,
        q_table = load_Qtable("1.pkl"),
        alpha=0.1,      # Learning speed-quality relation
        epsilon=0,    # Exploration rate
        gamma=0.95      # Importance of future/immediate rewards
    )

