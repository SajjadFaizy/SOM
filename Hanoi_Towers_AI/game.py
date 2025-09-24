from game_logic import Game
from q_brain import SOMPiBrain
from gui import HanoiGUI
import os, pickle

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
            print(f"Qtable loaded from: {filepath}")
        return q_table
    else:
        raise FileNotFoundError(f"The file '{filename}' does not exist in {qtables_dir}")

def play(num_disks, q_table):
    """ Runs the game with GUI """

    # Init game
    game = Game(num_disks)
    gui = HanoiGUI(num_disks, 3)
    
    state_num = 3 ** num_disks # Qty possible states
    actions = [(0,1), (0,2), (1,0), (1,2), (2,0), (2,1)] # Possible actions (source->target):
    action_num = len(actions) # Qty possible actions 

    print("\n\nPress enter to let the AI move")

    # Init AI
    q_brain = SOMPiBrain(state_num, action_num, q_table=q_table) # Instance Agent

    while True:
        
        state_index = game.get_state_index()

        # Get action from Q-Learning-Brain
        if not input():

            while True:
                try:
                    action = q_brain.get_action(state_index) # Choose action
                    break
                except:
                    ValueError("The AI tried to make a not valid move")

            source, target = actions[action] # Extract source and target from chosen action

            game.move_ring(source, target) # Move ring in game logic
            gui.moveRing(source, target) # Move ring in gui

            if game.is_solved(): break # Proof if Won

    print(" THE AI HAS SOLVED THE GAME !!!")

if __name__ == "__main__":
    play(num_disks = 3, q_table = load_Qtable("1.pkl"))