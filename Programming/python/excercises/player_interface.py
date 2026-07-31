from abc import ABC, abstractmethod
import random

class Player(ABC):
    def __init__(self):
        self.moves = []
        self.position = (0, 0)
        self.path = [self.position]

    def make_move(self):
        move_x, move_y = random.choice(self.moves)
        x,y = self.position
        self.position = (x + move_x, y + move_y)
        self.path.append(self.position)
        return self.position
    
    @abstractmethod
    def level_up(self):
        pass

class Pawn(Player):
    def __init__(self):
        super().__init__()
        self.moves = [
            (0, 1),  # Up
            (0, -1), # Down
            (-1 ,0), # Left
            (1, 0)   # right
            ]
    
    def level_up(self):
        if (1,1) not in self.moves:
            self.moves.extend([(1, 1), (-1, -1), (1, -1), (-1, 1)])
        else:
            return f"Diagonal Moves have already been added."

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
