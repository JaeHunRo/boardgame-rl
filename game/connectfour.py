"""Connect Four."""


from game import Game


class ConnectFour(Game):
    """Connect Four game class."""

    def __init__(self, rows=6, cols=7):
        """Construct new Connect Four game instance.

        The most commonly used Connect Four board size is 7 columns x 6 rows.
        Size variations include 8x7, 9x7, 10x7, 8x8
        """
        self.rows = rows
        self.cols = cols
        self.board = self.create_board(rows, cols)
        self.player = 'X'
        self.winner = None

    def create_board(self, rows, cols):
        """Create empty board of size rows x cols."""
        board = []
        for i in range(rows * cols):
            board.append('-')
        return board

    def reset(self):
        """Reset board between games."""
        self.board = self.create_board(self.rows, self.cols)
        self.player = 'X'
        self.winner = None

    def get_open_moves(self):
        """Returns list of available moves given current states and next states."""
        actions = []
        states = []
        for i, val in enumerate(self.board):
            if val == '-':
                actions.append(i)
                self.board[i] = self.player
                states.append(self.get_state(self.board))
                self.board[i] = '-'
        return states, actions

    def get_state(self, board):
        """Returns board state as String."""
        return ''.join(board)

    def is_win(self):
        """Check the board for win condition.

        Possible outputs are X, O, Draw, None.
        """
        # Convert to 2D array for ease of implementaiton
        grid = []
        for i in range(self.rows):
            grid.append([])
            for j in range(self.cols):
                grid[i].append(self.board[(i * self.cols) + j])

        # Check horizontal, vertical, and diagonal sequences for four in a row
        for i in range(self.rows):
            for j in range(self.cols):
                if j <= self.cols - 4:
                    # Horizontal
                    sequence = grid[i][j] + grid[i][j + 1] + grid[i][j + 2] + grid[i][j + 3]
                    if sequence == 'XXXX':
                        return 'X'
                    elif sequence == 'OOOO':
                        return 'O'
                if i <= self.rows - 4:
                    # Vertical
                    sequence = grid[i][j] + grid[i + 1][j] + grid[i + 2][j] + grid[i + 3][j]
                    if sequence == 'XXXX':
                        return 'X'
                    elif sequence == 'OOOO':
                        return 'O'
                if i <= self.rows - 4 and j <= self.cols - 4:
                    # Diagonal Right
                    sequence = grid[i][j] + grid[i + 1][j + 1] + grid[i + 2][j + 2] + grid[i + 3][j + 3]
                    if sequence == 'XXXX':
                        return 'X'
                    elif sequence == 'OOOO':
                        return 'O'
                if i <= self.rows - 4 and j >= 3:
                    # Diagonal Left
                    sequence = grid[i][j] + grid[i + 1][j - 1] + grid[i + 2][j - 2] + grid[i + 3][j - 3]
                    if sequence == 'XXXX':
                        return 'X'
                    elif sequence == 'OOOO':
                        return 'O'
        # Check Draw condition
        if '-' not in self.board:
            return 'Draw'

        # Unfinished game
        return None

    def is_valid_move(self, position):
        """Check that potential move is in a valid position.

        Valid means inbounds and not occupied.
        """
        if position >= 0 and position < len(self.board):
            return self.board[position] == '-'
        else:
            return False

    def make_move(self, position):
        """Makes move by setting position to player value.

        Also toggles player and returns is_win result.
        """
        self.board[position] = self.player
        self.player = 'O' if self.player == 'X' else 'X'
        return self.is_win()

    def print_board(self):
        s = ''
        for i in range(self.rows * self.cols):
            s += self.board[i] + ' '
            if ((i + 1) % self.cols == 0 and
                    (i + 1) < self.rows * self.cols):
                s += '\n'
        print(s)
        print('===============')

    def print_instructions(self):
        print('===============\n'
              'How to play:\n'
              'Possible moves are [0,M*N) where M is rows and N is cols\n'
              'Corresponding to these spaces on the board:\n\n'
              '0 | 1 | 2 | ... | N - 1\n'
              '.\n'
              '.\n'
              '.\n'
              '. | . | . | ... | M*N - 1\n')