# Author: Nicholas Gervais
# GitHub username: gervaisnOSU
# Date: 11/2/2025
# Description:

from AnimalGame import *
import unittest

#Unit Test Class
class TestAnimalGame(unittest.TestCase):
    """
    My class for all the test cases.
    """
    def game_creator(self):
        """
        Creates a new game instance before each test.
        """
        self.game = AnimalGame()

    # Test 1: Pieces only move valid distances
    def test_valid_distances(self):
        """
        Sliding pieces can move less than their full range, jumping pieces cannot.
        """
        # Test Okapi (distance of 4) for sliding 3 spaces
        self.game_creator()  # Reset game
        test_result = self.game.make_move("A1", "A4")
        self.assertTrue(test_result, "This should be true since a sliding unit can go less then their max.")

        # Test Okapi at max distance
        self.game_creator()  # Reset game
        test_result = self.game.make_move("A1", "A5")
        self.assertTrue(test_result, "This should be true since a sliding unit can go their max.")

        # Test Kinkajou for jumping their max of 3 squares diagonally
        self.game_creator() #Reset game
        test_result = self.game.make_move("C1", "F4")
        self.assertTrue(test_result, "Kinkajou should be able to make this move.")

        # Test Kinkajou for jumping only 2 spaces diagonally
        self.game_creator()  # Reset game
        test_result = self.game.make_move("C1", "E3")
        self.assertFalse(test_result, "Kinkajou should not be able to make this move.")

    # Test 2: Valid directional movement
    def test_valid_directions(self):
        """
        Pieces only move valid directions (diagonal pieces can also move one square orthogonally and orthogonal pieces can also move one square diagonally).
        """
        # Test Okapi can move 1 square diagonally
        self.game_creator()  # Reset game
        test_result = self.game.make_move("A1", "B2")
        self.assertTrue(test_result, "This should be true since all units can move 1 position in all directions.")

        # Test Okapi moving 2 squares diagonally
        self.game_creator()  # Reset game
        test_result = self.game.make_move("A1", "C3")
        self.assertFalse(test_result, "This should be false since Okapi is an orthogonal unit.")

        # Test whether Kinkajou can move 2 space orthogonally
        self.game_creator()  # Reset game
        test_result = self.game.make_move("C1", "C3")
        self.assertFalse(test_result, "This should be false since kinkajou's are diagonal units.")

    # Test 3: Blocking tests
    def test_blocking(self):
        """
        Sliding pieces are blocked by intervening pieces, jumping pieces are not.
        """
        # Test whether a sliding unit is blocked
        self.game_creator()  # Reset game
        self.game.make_move("B1", "A2")
        self.game.make_move("A7", "A6")
        test_result = self.game.make_move("A1", "A3")
        self.assertFalse(test_result, "This should be false since sliding units cannot move through units.")

        # Test whether a jumping unit is not blocked
        self.game_creator()  # Reset game
        self.game.make_move("D1", "D2")
        self.game.make_move("A7", "A6")
        test_result = self.game.make_move("C1", "F4")
        self.assertTrue(test_result, "This should be true since jumping units can move through units.")

    # Test 4: Captures
    def test_captures(self):
        """
        Captures are handled correctly, including that players cannot capture their own pieces.
        """
        # Test whether you can capture your own unit
        self.game_creator()  # Reset game
        test_result = self.game.make_move("A1", "B1")
        self.assertFalse(test_result, "This should be false since you cannot capture your own unit.")

        # Test whether you can capture an enemy unit
        self.game_creator()  # Reset game
        piece = self.game.get_board().get_spaces()["A1"].get_occupant()
        self.game.make_move("A1", "A4")
        self.game.make_move("A7", "A4")
        test_result = piece.get_piece_state()
        self.assertEqual(test_result, "Dead")

    #Test 5: Turn order
    def test_turn_order(self):
        """
        Turn order is handled correctly
        """
        # Amethyst tries to go first
        self.game_creator() # Reset game
        test_result = self.game.make_move('A7', 'A6')
        self.assertFalse(test_result, "Amethyst cannot be able to go first")

        # Tangerine goes then amethyst can go
        self.game_creator()  # Reset game
        self.game.make_move("A1", "A4")
        test_result = self.game.make_move('A7', 'A6')
        self.assertTrue(test_result, "Tangerine goes first and then Amethyst can go.")

    #Test 6: game state
    def test_game_state(self):
        """
        The get_game_state() method correctly reports the game state.
        """

        # Tests whether the game is unfinished at the start of the game
        self.game_creator() # Reset game
        test_result = self.game.get_game_state()
        self.assertEqual(test_result, "UNFINISHED")

        # Tests whether game gets won
        self.game_creator()  # Reset game
        self.game.make_move("A1", "A5")
        self.game.make_move("D7", "B5")
        self.game.make_move("A5", "B5")
        test_result = self.game.get_game_state()
        self.assertEqual(test_result, "TANGERINE_WON")

#Runs the unit tests
if __name__ == "__UnitTests__":
    test = TestAnimalGame()
    test.test_valid_distances()
    test.test_valid_directions()
    test.test_blocking()
    test.test_captures()
    test.test_turn_order()
    test.test_game_state()
