#This py file contains my code for the end of term project. It is a chess-like game that is run mostly through the AnimalGame class.
# I would classify the rest as infrastructure while the AnimalGame class is the main game code. Overall, the AnimalGame class calls all the other classes or
# at least classes that call the ones it doesn't.

class AnimalGame:
    """
    This class is the main game loop class, which communicates with all other classes.
    It needs all information from other classes to effectively run the game.
    What it contains (descriptions of each found in their respective methods):
    - __init__
    - change_player_turn
    - get_game_state
    - set_game_state
    - get_players
    - add_players_pieces_to_board
    - make_move
    - move_validity_checker
    - path_is_clear
    - pos_to_coordinates
    """
    def __init__(self):
        """
        Initializes all the data members for the AnimalGame class including current turn, game state, players, board, create game board spaces,
        add player pieces to board, and display game board.
        Note: display gameboard was just for testing purposes and a personal challenge.
        """
        # 1 is Tangerine, -1 is Amethyst. Initializes as Tangerines turn.
        self._player_turn = 1

        # Game is unfinished when game is starting.
        self._game_state = "UNFINISHED"

        # Dictionary of players.
        self._players = {1 : Player("Tangerine", True), -1 : Player("Amethyst", False)}

        # Creates an empty board object from Board class for the game.
        self._board = Board()

        # Creates the game spaces objects for the board.
        self._board.create_game_board_spaces()

        # Creates and adds player pieces to the board.
        self._add_players_pieces_to_board()

        # Displays the board for fun, but does not update throughout game since the instructions did not say to use a loop.
        self._board.display_game_board()

    def change_player_turn(self):
        """
        Changes the turn by multiplying the number by -1.
        Note: self._player_turn is the index for self._players.
        """
        # Swaps current turn to opposite player.
        self._player_turn = self._player_turn*-1

    def get_game_state(self):
        """
        Returns the game state as a string
        """
        return self._game_state

    def set_game_state(self, winner_player_index):
        """
        Sets the game state based on the project requirements using string interpolation.
        """
        self._game_state = f"{self._players[winner_player_index].get_name().upper()}_WON"

    def get_players(self):
        """
        Returns the dictionary of players.
        """
        return self._players

    def _add_players_pieces_to_board(self):
        """
        This function creates game pieces and adds them to the board created in init.
        """
        # Sets up Player 1's (Tangerine) pieces
        self._board.setup_game_board("A1", Okapi("A1", self._players[1]))
        self._board.setup_game_board("B1", Wombat("B1", self._players[1]))
        self._board.setup_game_board("C1", Kinkajou("C1", self._players[1]))
        self._board.setup_game_board("D1", Cuttlefish("D1", self._players[1]))
        self._board.setup_game_board("E1", Kinkajou("E1", self._players[1]))
        self._board.setup_game_board("F1", Wombat("F1", self._players[1]))
        self._board.setup_game_board("G1", Okapi("G1", self._players[1]))

        # Sets up Player -1's (Amethyst) pieces
        self._board.setup_game_board("A7", Okapi("A7", self._players[-1]))
        self._board.setup_game_board("B7", Wombat("B7", self._players[-1]))
        self._board.setup_game_board("C7", Kinkajou("C7", self._players[-1]))
        self._board.setup_game_board("D7", Cuttlefish("D7", self._players[-1]))
        self._board.setup_game_board("E7", Kinkajou("E7", self._players[-1]))
        self._board.setup_game_board("F7", Wombat("F7", self._players[-1]))
        self._board.setup_game_board("G7", Okapi("G7", self._players[-1]))

    def make_move(self, initial_pos, desired_pos):
        """
        This method calls my move_validity_checker to test whether a move is valid, then continues when a valid move is selected.
        """
        # Ensures that the input has uppercase letters
        initial_pos = initial_pos.upper()
        desired_pos = desired_pos.upper()

        # Make variables to save time and room.
        spaces = self._board.get_spaces()
        game_piece = spaces[initial_pos].get_occupant()
        other_piece = spaces[desired_pos].get_occupant()

        # Verifies the move is valid.
        if self.move_validity_checker(initial_pos, desired_pos, spaces, game_piece, other_piece) is False:
            return False
        else:
            # Deletes piece from desired location if there is one.
            if other_piece is not None:
                # Check for victory.
                if other_piece.get_symbol() == "C":
                    self.set_game_state(self._player_turn)
                    return True
                other_piece.set_piece_state_dead()

            #Moves the piece to the new space
            spaces[desired_pos].set_occupant(game_piece)
            spaces[initial_pos].set_occupant(None)
            game_piece.set_position(desired_pos)

            #Swaps turns by multiplying by -1
            self.change_player_turn()

            return True

    def move_validity_checker(self, initial_pos, desired_pos, spaces, game_piece, other_piece):
        """
        This method does most of the validity information using from individual game pieces classes.
        """
        # If the initial position does not have a piece then it's an invalid move.
        if game_piece is None:
            return False

        # Useful variables for validity verification.

        # Gets the piece's specific movement distance.
        piece_distance = game_piece.get_distance()
        # Gets the piece's specific direction type.
        piece_direction = game_piece.get_direction_type()
        # Gets the piece's specific movement type.
        piece_locomotion = game_piece.get_locomotion()
        # Gets the omnidirectional movement which is 1 for all pieces.
        piece_omni_directional_distance = game_piece.get_omni_directional_distance()

        # Convert to coordinates so math is possible.
        initial_x, initial_y = self.pos_to_coordinates(initial_pos)
        final_x, final_y = self.pos_to_coordinates(desired_pos)

        # Calculate the x and y distance.
        x_distance = abs(final_x - initial_x)
        y_distance = abs(final_y - initial_y)

        # Determines whether the movement is orthogonal using XOR. If only x distance or y distance is true then it's orthogonal.
        movement_is_orthogonal = (x_distance == 0) ^ (y_distance == 0)

        # Determines whether the movement is diagonal.
        movement_is_diagonal = x_distance == y_distance and x_distance > 0

        # If the piece in the initial position is not the current players piece then it's an invalid move.
        if game_piece.get_player() is not self._players[self._player_turn]:
            return False

        # If the game is over then it is an invalid move.
        if self._game_state != "UNFINISHED":
            return False

        # If the move starts and ends on the same tile it is an invalid move.
        if x_distance == 0 and y_distance == 0:
            return False

        # If the piece tries to move too far then it is an invalid move.
        if x_distance > piece_distance or y_distance > piece_distance:
            return False

        # If the piece at the destination is owned by the player whose turn it currently is, then it is an invalid move.
        if other_piece is not None and other_piece.get_player() == self._players[self._player_turn]:
            return False

        # Orthogonal movement.
        if movement_is_orthogonal:
            # If the pieces main movement method is orthogonal, then it can move its full movement.
            if piece_direction == "orthogonal":
                    # If the pieces locomotion is sliding, then we must check the path.
                    if piece_locomotion == "sliding":
                        # If the path is clear the move is valid.
                        if self.path_is_clear(spaces, initial_pos, initial_x, initial_y, final_x, final_y):
                            return True
                        # If the path is not clear, the move is not valid.
                        else:
                            return False
                    # If the pieces locomotion is not sliding then it is jumping.
                    else:
                        # Jumping pieces must move their full distance
                        if x_distance == piece_distance or y_distance == piece_distance:
                            return True
                        else:
                            return False
            # If the pieces main movement is not orthogonal, it can move a max of 1 tile.
            else:
                # If the movement is 1, then the move is valid at this point.
                if piece_omni_directional_distance == x_distance or piece_omni_directional_distance == y_distance:
                    return True
                # If the movement is greater than 1 at this point in the code, the move is not valid.
                else:
                    return False

        # Diagonal movement.
        if movement_is_diagonal:
            # If the pieces main movement method is diagonal, then it can move its full movement.
            if piece_direction == "diagonal":
                    # If the pieces locomotion is sliding, then we must check the path.
                    if piece_locomotion == "sliding":
                        # If the path is clear the move is valid.
                        if self.path_is_clear(spaces, initial_pos, initial_x, initial_y, final_x, final_y):
                            return True
                        # If the path is not clear, the move is not valid.
                        else:
                            return False
                    # If the pieces locomotion is not sliding then it is jumping.
                    else:
                        # Jumping pieces must move their full distance
                        if x_distance == piece_distance or y_distance == piece_distance:
                            return True
                        else:
                            return False
            # If the pieces main movement is not diagonal, it can move a max of 1 tile.
            else:
                # If the movement is 1, then the move is valid at this point.
                if piece_omni_directional_distance == x_distance or piece_omni_directional_distance == y_distance:
                    return True
                # If the movement is greater than 1 at this point in the code, the move is not valid.
                else:
                    return False

        # If it is neither orthogonal movement or diagonal movement, then the movement is invalid.
        return False

    def path_is_clear(self, spaces, initial_pos, initial_x, initial_y, final_x, final_y):
        """
        This method determines whether the path for a sliding piece is clear or blocked.
        """
        # if this is positive we are moving up, else down.
        y_direction = final_y - initial_y
        # if this is positive we are moving right, else left.
        x_direction = final_x - initial_x

        # If moving in the y direction.
        if initial_x == final_x:
            # Need to determine whether we're moving up or down.
            if y_direction > 0:
                direction_counter = 1
            else:
                direction_counter = -1
            # Check each space between the initial position and desired position.
            for y_coord in range(initial_y + direction_counter, final_y, direction_counter):
                if spaces[f"{initial_pos[0]}{y_coord}"].get_occupant() is not None:
                    return False
            return True

        # If moving in the x direction.
        if initial_y == final_y:
            # Need to determine whether we're moving right or left.
            if x_direction > 0:
                direction_counter = 1
            else:
                direction_counter = -1
                # Check each space between the initial position and desired position.
            for x_coord in range(initial_x + direction_counter, final_x, direction_counter):
                if spaces[f"{self._board.get_columns()[x_coord]}{initial_pos[1]}"].get_occupant() is not None:
                    return False
            return True

        # If moving diagonally.
        else:
            # Need to determine whether we're moving right or left.
            if x_direction > 0:
                direction_counter_x = 1
            else:
                direction_counter_x = -1
            # Need to determine whether we're moving up or down.
            if y_direction > 0:
                direction_counter_y = 1
            else:
                direction_counter_y = -1

            # Find first spot to check.
            x_coord = initial_x + direction_counter_x
            y_coord = initial_y + direction_counter_y

            # Check each spot diagonally in the correct direction until you reach intended position.
            while x_coord != final_x and y_coord != final_y:
                if spaces[f"{self._board.get_columns()[x_coord]}{y_coord}"].get_occupant() is not None:
                    return False
                # Increment to the next position diagonally using our direction counter.
                x_coord += direction_counter_x
                y_coord += direction_counter_y

            # If the check makes it here, then there is nothing blocking the movement.
            return True

    def pos_to_coordinates(self, position):
        """
        This method converts the position label of each space or piece into coordinates which are much easier to work with.
        """
        x = ord(position[0]) - ord("A") # x-coordinate
        y = int(position[1]) # y-coordinate
        return x, y

    def get_board(self):
        """
        Returns the board for testing purposes.
        """
        return self._board

class Player:
    """
    This is a simple player class to keep track of turns and it holds a name.
    """
    def __init__(self, name, is_turn):
        """
        Initializes a player object with a name and turn status.
        """
        self._name = name
        self._is_turn = is_turn

    def set_is_turn(self, turn_status):
        """
        Sets the turn status.
        """
        self._is_turn = turn_status

    def get_name(self):
        """
        Returns the name.
        """
        return self._name

class Board:
    """
    This class, called from AnimalGame init, creates the game board including the node spaces for the pieces to go.
    """

    def __init__(self):
        """
        This contains the initial possible values for the rows and columns, and constructs a spaces dictionary.
        """
        self._rows = ["1", "2", "3", "4", "5", "6", "7"]
        self._columns = ["A", "B", "C", "D", "E", "F", "G"]
        self._spaces = {}

    def get_spaces(self):
        """
        Returns the spaces dictionary.
        """
        return self._spaces

    def get_columns(self):
        """
        Returns the columns list.
        """
        return self._columns

    def create_game_board_spaces(self):
        """
        This method, called from AnimalGame, creates the game board spaces using the Space class.
        """
        for column in self._columns:
            for row in self._rows:
                space = Space(row, column, None)
                self._spaces[space.get_label()] = space

    def setup_game_board(self, label, piece):
        """
        Adds the pieces to board sides.
        """
        self._spaces[label].set_occupant(piece)

    def display_game_board(self):
        """
        This method is a simple one that creates a simple display for the game. I could have had it autoupdate the display, but it was not
        in the instructions. I also figured this would be easier to grade if I didn't force you guys into a looping game.
        """
        print("   A   B   C   D   E   F   G")
        for row in reversed(self._rows):
            game_board_str = f"{row} "
            for col in self._columns:
                space = self._spaces[col + row]
                occupant = space.get_occupant()
                if occupant is None:
                    game_board_str += "[ ] "
                else:
                    game_board_str += f"[{occupant.get_symbol()}] "
            print(game_board_str)

class Space:
    """
    This class will create spaces for the game board..
    """

    def __init__(self, row, column, occupant):
        """
        Constructs an unoccupied space with a label.
        """
        # This is None by default which means the space is empty by default, this can have a game piece.
        self._occupant = occupant
        self._row = row
        self._column = column
        self._label = column + row

    def get_occupant(self):
        """
        Returns the piece that is occupying this space, or None if there is no piece.
        """
        return self._occupant

    def set_occupant(self, occupant):
        """
        This method sets an occupant to the space. Input should be a piece object, or None.
        """
        self._occupant = occupant

    def get_row(self):
        """
        Returns the space row.
        """
        return self._row

    def get_column(self):
        """
        Returns the space column.
        """
        return self._column

    def get_label(self):
        """
        Returns the space label
        """
        return self._label

class Piece:
    """
    This class creates game piece objects.
    Information about game pieces:
    -A piece can move a certain distance
    -A piece can move that distance using their specific direction or 1 distance in the other direction
    -Directions:
        Orthogonal and Diagonal
    -Locomotion rules:
        Sliding - Can move any nonzero number of squares up to its distance in a straight line. Cannot move past another piece (gets blocked)
        Jumping - Has to move its full movement in a straight line, cannot be blocked.
    -A piece cannot move to a square with an ally piece, if a piece goes to a square with an enemy piece, then you capture the piece and remove it from the game.
    """
    def __init__(self, direction_type, distance, locomotion, position, player, symbol):
        """"""
        # Pieces can either be alive or dead based on whether they've been captured.
        self._piece_state = "Alive"
        # All pieces need a position on the board unless they're dead.
        self._position = position
        # All pieces need a direction type.
        self._direction_type = direction_type
        # All pieces have a max distance.
        self._distance = distance
        # All pieces can move 1 space in all directions.
        self._omni_directional_distance = 1
        # All piece have a locomotion type.
        self._locomotion = locomotion
        # Pieces need an assigned player to determine who has what
        self._player = player
        # This is purely for display.
        self._symbol = symbol

    def get_piece_state(self):
        """
        Returns the piece state.
        """
        return self._piece_state

    def set_piece_state_dead(self):
        """
        This Method sets the piece state as Dead and makes its position None.
        Note: The state is alive by default, so you only ever need to change the pieces state to dead.
        """
        self._piece_state = "Dead"
        self._position = None

    def get_position(self):
        """
        Returns the pieces position.
        """
        return self._position

    def set_position(self, new_position):
        """
        Sets the pieces position to a new position.
        """
        self._position = new_position

    def get_direction_type(self):
        """
        Returns the pieces direction type.
        """
        return self._direction_type

    def get_distance(self):
        """
        Returns the pieces maximum distance.
        """
        return self._distance

    def get_omni_directional_distance(self):
        """
        Returns the pieces omnidirectional distance.
        Note: This is the same for all pieces, 1 in all directions.
        """
        return self._omni_directional_distance

    def get_locomotion(self):
        """
        Returns the pieces locomotion.
        """
        return self._locomotion

    def get_player(self):
        """
        Returns the pieces associated player.
        """
        return self._player

    def get_symbol(self):
        """
        Returns the pieces associated symbol.
        """
        return self._symbol

class Okapi(Piece):
    """
    Inherits from Piece class since this is a game piece but with more specific information.
    Piece Information:
    Direction - orthogonal
    Distance - 4 spaces
    Locomotion - sliding
    Symbol = o
    """
    def __init__(self, position, player, symbol = "o"):
        """
        Takes the inherited Piece class constructor and passes in custom information intended to make move verification easy.
        """
        super().__init__("orthogonal", 4, "sliding", position, player, symbol)

class Wombat(Piece):
    """
    Inherits from Piece class since this is a game piece but with more specific information.
    Piece Information:
    Direction - orthogonal
    Distance - 1 space
    Locomotion - jumping
    Symbol = w
    """
    def __init__(self, position, player, symbol = "w"):
        """
        Takes the inherited Piece class constructor and passes in custom information intended to make move verification easy.
        """
        super().__init__("orthogonal", 1, "jumping", position, player, symbol)

class Kinkajou(Piece):
    """
    Inherits from Piece class since this is a game piece but with more specific information.
    Piece Information:
    Direction - diagonal
    Distance - 3 spaces
    Locomotion - jumping
    Symbol = k
    """
    def __init__(self, position, player, symbol = "k"):
        """
        Takes the inherited Piece class constructor and passes in custom information intended to make move verification easy.
        """
        super().__init__("diagonal", 3, "jumping", position, player, symbol)

class Cuttlefish(Piece):
    """
    Inherits from Piece class since this is a game piece but with more specific information.
    Piece Information:
    Lose this piece and you lost the game
    Direction - diagonal
    Distance - 2 spaces
    Locomotion - sliding
    Symbol = C
    """
    def __init__(self, position, player, symbol = "C"):
        """
        Takes the inherited Piece class constructor and passes in custom information intended to make move verification easy.
        """
        super().__init__("diagonal", 2, "sliding", position, player, symbol)
