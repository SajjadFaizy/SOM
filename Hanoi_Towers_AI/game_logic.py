import numpy as np
class Game:
    """ Game rules of Towers of Hanoi """
    def __init__(self, num_disks=3):
        self.num_disks = num_disks
        self.towers = [np.array([i for i in range(num_disks, 0, -1)]), np.array([]), np.array([])] # The bigger the disk, the smaller the index, 0 excluded in range()
        self.history = np.array([0])
    def get_state(self):
        return [tower.copy() for tower in self.towers]
    def get_state_index(self):
        state_index = 0
        num_disks = sum(len(tower) for tower in self.towers)
        disk_positions = [-1] * num_disks # Declare variable
        # Allocate tower indeces (disk_positions[i]) to each disk (i)
        for tower_index, tower in enumerate(self.towers):
            for disk in tower:
                disk_positions[int(disk) - 1] = tower_index
        # Convert positions of disks into index in base 3
        for position in disk_positions:
            state_index = state_index * 3 + position # ~ index_big * 3^n + index_mid * 3^n-1 + ... + index_small * 3^0
        return state_index
    def move_ring(self, source, target):
        # Chosen Towers valid?
        if not (0 <= source <= 2 and 0 <= target <= 2): # If source inexistent -> error
            raise ValueError("The peg's indexes must be between 0 and 2")
        if self.towers[source].size == 0: # If source empty -> error
            raise ValueError(f"The peg {source} is empty")
        # Moving Ring
        disk = self.towers[source][-1]
        # Valid Move?
        if self.towers[target].size > 0 and self.towers[target][-1] < disk: # If upper disk on target is smaller
            raise ValueError(f"It's not possible to lay the disk {disk} on a smaller disk")
        # Move
        self.towers[source] = self.towers[source][:-1] # Delete disk from source
        self.towers[target] = np.append(self.towers[target], disk) # Add disk to target
        # Update History
        self.history = np.append(self.history, self.get_state_index())
    def is_solved(self):
        return (self.towers[2].size == self.num_disks and 
                self.towers[0].size == 0 and
                self.towers[1].size == 0)
    def __str__(self):
        return "--".join([f"{tower}" for tower in self.towers])
