# Here we are going to write John Conways Game of Life. 
import numpy as np


# The Concept is 
# each state is an n dim array of tuples (x,y,1/0) where 1 is on and 0 is off
# Rowwise schema 
# if it were a chess board then a1 is 0,0 h1 is 7,0 a8 is 0,7 and h8 is 7,7



# This object will be a state object. 
# It will be a map with
#   KEY = FRAME NUMBER
#   VALUE = STATE ARRAY

class GameOfLife():

    def __init__(self, n_rows: int, n_cols: int, live_cells: list[tuple[int,int]] = None):
        """
            INPUTS
            n_rows: number of rows on the board 
            n_cols: number of columns on the board
            live_cells: list of tuples (x,y) for each cell to be turned on
        """

        self.n_rows_ = n_rows
        self.n_cols_ = n_cols
        self.state_ = np.zeros((n_rows, n_cols))
        self.history_ = {} # python dict of the states 
        self.n_frames_ = len(self.history_)

        #turn the cells ON
        if (live_cells is not None):
            for cell in live_cells:
                assert(cell[0] < self.n_rows_)
                assert(cell[1] < self.n_cols_)
                self.state_[cell[0]][cell[1]] = 1

        # save the initial state
        self.history_[0] = self.state_
        self.n_frames_ += 1

    def get_info(self):
        print(f"num rows {self.n_rows_}")
        print(f"num cols {self.n_cols_}")
        print(f"num frames {self.n_frames_}")
        sum = 0
        for row in range(self.n_rows_):
            for col in range(self.n_cols_):
                sum += self.state_[row][col]
        print(f"num live cells {sum}")
    
    def get_num_livers(self):
        sum = 0
        for row in range(self.n_rows_):
            for col in range(self.n_cols_):
                sum += self.state_[row][col]
        print(f"num live cells {sum}")

    def num_living_neighbors(self, num_frame:int):
        '''
        This function returns a numpy array where each value represents the number of neighbors that frames cell has
        INPUTS:
        --------------
        num_frame: which frame to examine
        RETURNS:
        ---------------- 
        a numpy 2D array where each element is the number of alive eigbors that cell has at that frame.
        '''
        num_live_neighbors_board = np.zeros((self.n_rows_, self.n_cols_))
        print(f"frame \n {num_frame -1} \n and the history at that frame \n {self.history_[num_frame -1]} \n ")
        padded_frame = np.pad(self.history_[num_frame -1], 1)

        for row in range(self.n_rows_):
            for col in range(self.n_cols_):
                num_live_neighbors_board[row][col] = np.sum(padded_frame[row:row+3, col: col+3]) - padded_frame[row+1, col+1]

        return num_live_neighbors_board

    def update(self):

        new_state = np.zeros((self.n_rows_, self.n_cols_));
        live_neighbors = self.num_living_neighbors(self.n_frames_)

        for row in range(self.n_rows_):
            for col in range(self.n_cols_):
                n_live_neighbors = live_neighbors[row][col] 

                # How to Die
                if ( self.state_[row][col] == 1 ):
                    if n_live_neighbors < 2:
                        new_state[row][col] = 0
                    elif n_live_neighbors > 3:
                        new_state[row][col] = 0
                    else: # surviving
                        new_state[row][col] = 1

                # how to come to life 
                if ( self.state_[row][col] == 0 ):
                    if n_live_neighbors == 3:
                        new_state[row][col] = 1

        
        self.history_[self.n_frames_] = new_state
        self.state_ = new_state 
        self.n_frames_ += 1 
        self.get_num_livers()

    def run(self, num_updates: int):
        for i in range(num_updates):
            self.update()
        print('Game Complete')


    def get_game(self):
        print("[frame #] ==> 2D-nparray")
        return self.history_


def main():
    # BOARD DIMENSIONS
    row = 5
    col = 5
    # INITIAL LIVING CELLS 
    live_cells = [(0,0), (1,0), (1,1), (2,2)]
    # NUMBER OF STEPS 
    steps = 10 

    gol = GameOfLife(row, col, live_cells)
    gol.run(steps)
    gol.get_game()


if __name__ == "__main__":
    main()

