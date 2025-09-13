import unittest
import os
import tempfile
import shutil
import chess
from unittest.mock import patch, MagicMock, mock_open
from chs.client.runner import Client
from chs.engine.stockfish import Engine
from chs.utils.core import Levels


class TestTermuxIntegration(unittest.TestCase):
    """Integration tests for CHS chess game in Termux environment"""
    
    def setUp(self):
        """Set up test environment with mock Stockfish"""
        self.temp_dir = tempfile.mkdtemp()
        self.mock_stockfish_path = os.path.join(self.temp_dir, 'stockfish')
        # Create a dummy stockfish executable
        with open(self.mock_stockfish_path, 'w') as f:
            f.write('#!/bin/bash\necho "Stockfish mock"')
        os.chmod(self.mock_stockfish_path, 0o755)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('chess.engine.SimpleEngine.popen_uci')
    def test_termux_game_initialization(self, mock_popen):
        """Test complete game initialization in Termux environment"""
        # Mock engine setup
        mock_engine = MagicMock()
        mock_popen.return_value = mock_engine
        
        # Simulate Termux environment
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            with patch('shutil.which') as mock_which:
                mock_which.return_value = self.mock_stockfish_path
                
                # Test client initialization
                client = Client(Levels.ONE, chess.WHITE)
                
                # Verify engines were created
                self.assertIsNotNone(client.engine)
                self.assertIsNotNone(client.hint_engine)
                
                # Verify initial game state
                self.assertEqual(client.play_as, chess.WHITE)
                self.assertIsInstance(client.board, chess.Board)
                self.assertTrue(client.board.san_move_stack_white == [])
                self.assertTrue(client.board.san_move_stack_black == [])
    
    @patch('chess.engine.SimpleEngine.popen_uci')
    def test_termux_move_validation(self, mock_popen):
        """Test move validation and parsing in Termux environment"""
        mock_engine = MagicMock()
        mock_popen.return_value = mock_engine
        
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            with patch('shutil.which') as mock_which:
                mock_which.return_value = self.mock_stockfish_path
                
                client = Client(Levels.ONE, chess.WHITE)
                
                # Test valid moves
                valid_moves = ['e4', 'Nf3', 'd4', 'c4']
                for move in valid_moves:
                    try:
                        parsed_move = client.board.parse_san(move)
                        self.assertIsNotNone(parsed_move, f"Failed to parse valid move: {move}")
                    except ValueError:
                        # Reset board for next move test
                        client.board = chess.Board()
    
    @patch('chess.engine.SimpleEngine.popen_uci')
    def test_termux_hint_system(self, mock_popen):
        """Test hint system functionality in Termux"""
        mock_engine = MagicMock()
        mock_move_result = MagicMock()
        mock_move_result.move = chess.Move.from_uci('e2e4')
        mock_engine.play.return_value = mock_move_result
        mock_popen.return_value = mock_engine
        
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            with patch('shutil.which') as mock_which:
                mock_which.return_value = self.mock_stockfish_path
                
                client = Client(Levels.ONE, chess.WHITE)
                
                # Test hint functionality
                hint = client.hint_engine.play(client.board, 1.000)
                self.assertIsNotNone(hint)
                self.assertIsNotNone(hint.move)
    
    @patch('chess.engine.SimpleEngine.popen_uci')
    def test_termux_engine_configuration(self, mock_popen):
        """Test engine configuration for different difficulty levels in Termux"""
        mock_engine = MagicMock()
        mock_popen.return_value = mock_engine
        
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            with patch('shutil.which') as mock_which:
                mock_which.return_value = self.mock_stockfish_path
                
                # Test different difficulty levels
                for level in [Levels.ONE, Levels.FOUR, Levels.EIGHT]:
                    with self.subTest(level=level):
                        engine = Engine(level)
                        
                        # Verify engine was configured with correct skill level
                        mock_engine.configure.assert_called()
                        configure_args = mock_engine.configure.call_args[0][0]
                        self.assertIn('Skill Level', configure_args)
    
    @patch('chess.engine.SimpleEngine.popen_uci')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_termux_user_interaction(self, mock_print, mock_input, mock_popen):
        """Test user input handling in Termux environment"""
        mock_engine = MagicMock()
        mock_move_result = MagicMock()
        mock_move_result.move = chess.Move.from_uci('e7e5')
        mock_engine.play.return_value = mock_move_result
        mock_popen.return_value = mock_engine
        
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            with patch('shutil.which') as mock_which:
                mock_which.return_value = self.mock_stockfish_path
                
                client = Client(Levels.ONE, chess.WHITE)
                
                # Test valid move input
                mock_input.return_value = 'e4'
                
                try:
                    # This would normally run the game loop, but we'll just test move making
                    move = client.board.parse_san('e4')
                    client.board.push(move)
                    
                    # Verify move was made
                    self.assertEqual(len(client.board.move_stack), 1)
                    
                except Exception as e:
                    self.fail(f"User interaction test failed: {e}")
    
    @patch('chess.engine.SimpleEngine.popen_uci')
    def test_termux_game_state_management(self, mock_popen):
        """Test game state management and move tracking in Termux"""
        mock_engine = MagicMock()
        mock_popen.return_value = mock_engine
        
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            with patch('shutil.which') as mock_which:
                mock_which.return_value = self.mock_stockfish_path
                
                client = Client(Levels.ONE, chess.WHITE)
                
                # Test initial state
                self.assertFalse(client.board.is_game_over())
                self.assertEqual(len(client.board.move_stack), 0)
                
                # Make some moves
                moves = ['e4', 'e5', 'Nf3', 'Nc6']
                for i, move in enumerate(moves):
                    parsed_move = client.board.parse_san(move)
                    
                    # Track move in appropriate stack
                    if i % 2 == 0:  # White move
                        client.board.san_move_stack_white.append(client.board.san(parsed_move))
                    else:  # Black move
                        client.board.san_move_stack_black.append(client.board.san(parsed_move))
                    
                    client.board.push(parsed_move)
                
                # Verify game state
                self.assertEqual(len(client.board.move_stack), 4)
                self.assertEqual(len(client.board.san_move_stack_white), 2)
                self.assertEqual(len(client.board.san_move_stack_black), 2)
    
    def test_termux_error_handling_no_stockfish(self):
        """Test proper error handling when Stockfish is not available in Termux"""
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            with patch('shutil.which') as mock_which:
                mock_which.return_value = None
                
                with patch('os.path.exists') as mock_exists:
                    mock_exists.return_value = False
                    
                    with patch('chess.engine.SimpleEngine.popen_uci') as mock_popen:
                        mock_popen.side_effect = FileNotFoundError("No such file")
                        
                        with self.assertRaises(RuntimeError) as context:
                            Engine(Levels.ONE)
                        
                        error_msg = str(context.exception)
                        self.assertIn("Termux", error_msg)
                        self.assertIn("pkg install stockfish", error_msg)
    
    @patch('platform.machine')
    @patch('chess.engine.SimpleEngine.popen_uci')
    def test_termux_arm_performance(self, mock_popen, mock_machine):
        """Test performance considerations for ARM devices in Termux"""
        mock_engine = MagicMock()
        mock_popen.return_value = mock_engine
        mock_machine.return_value = 'aarch64'
        
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            with patch('shutil.which') as mock_which:
                mock_which.return_value = self.mock_stockfish_path
                
                # Test that low difficulty levels work well on ARM
                client = Client(Levels.ONE, chess.WHITE)
                
                # Verify engines are configured (main engine and hint engine)
                self.assertEqual(mock_engine.configure.call_count, 2)
                
                # Check the first configure call (main engine with level 1)
                first_call_args = mock_engine.configure.call_args_list[0][0][0]
                
                # Check that Hash and Threads are set for mobile optimization
                self.assertIn('Hash', first_call_args)
                self.assertIn('Threads', first_call_args)
                self.assertEqual(first_call_args['Hash'], 16)
                self.assertEqual(first_call_args['Threads'], 1)
                
                # Check skill level is reasonable for level 1  
                skill_level = first_call_args.get('Skill Level', 0)
                self.assertEqual(skill_level, 1, "Level 1 should map to skill level 1")
    
    @patch('chess.engine.SimpleEngine.popen_uci')
    def test_termux_cleanup_on_exit(self, mock_popen):
        """Test proper resource cleanup when game exits in Termux"""
        mock_engine = MagicMock()
        mock_popen.return_value = mock_engine
        
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            with patch('shutil.which') as mock_which:
                mock_which.return_value = self.mock_stockfish_path
                
                client = Client(Levels.ONE, chess.WHITE)
                
                # Simulate game ending
                client.engine.done()
                client.hint_engine.done()
                
                # Verify engines were properly closed
                self.assertEqual(mock_engine.quit.call_count, 2)


if __name__ == '__main__':
    unittest.main()