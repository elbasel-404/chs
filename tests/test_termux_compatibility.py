import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from chs.engine.stockfish import is_termux, get_system_stockfish, get_engine_path


class TestTermuxCompatibility(unittest.TestCase):
    """Test Termux-specific compatibility features"""
    
    def test_termux_detection_with_prefix(self):
        """Test Termux detection via PREFIX environment variable"""
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            self.assertTrue(is_termux())
    
    def test_termux_detection_with_data_directory(self):
        """Test Termux detection via data directory existence"""
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            self.assertTrue(is_termux())
            mock_exists.assert_called_with('/data/data/com.termux')
    
    def test_not_termux(self):
        """Test that normal Linux environment is not detected as Termux"""
        with patch.dict(os.environ, {}, clear=True):
            with patch('os.path.exists') as mock_exists:
                mock_exists.return_value = False
                self.assertFalse(is_termux())
    
    def test_system_stockfish_detection(self):
        """Test system Stockfish detection"""
        with patch('shutil.which') as mock_which:
            mock_which.return_value = '/usr/bin/stockfish'
            self.assertEqual(get_system_stockfish(), '/usr/bin/stockfish')
            
            mock_which.return_value = None
            self.assertIsNone(get_system_stockfish())
    
    def test_environment_variable_override(self):
        """Test that CHS_STOCKFISH_PATH environment variable works"""
        test_path = '/custom/path/to/stockfish'
        with patch.dict(os.environ, {'CHS_STOCKFISH_PATH': test_path}):
            with patch('os.path.exists') as mock_exists:
                mock_exists.return_value = True
                self.assertEqual(get_engine_path(), test_path)
    
    def test_system_stockfish_preference(self):
        """Test that system stockfish is preferred over bundled binary"""
        with patch('shutil.which') as mock_which:
            mock_which.return_value = '/usr/games/stockfish'
            with patch.dict(os.environ, {}, clear=True):
                path = get_engine_path()
                self.assertEqual(path, '/usr/games/stockfish')
    
    @patch('platform.system')
    @patch('platform.machine')
    def test_arm_architecture_detection(self, mock_machine, mock_system):
        """Test ARM architecture detection for Termux compatibility"""
        mock_system.return_value = 'Linux'
        mock_machine.return_value = 'aarch64'
        
        with patch('shutil.which') as mock_which:
            mock_which.return_value = '/system/stockfish'
            path = get_engine_path()
            self.assertEqual(path, '/system/stockfish')
    
    def test_bundled_binary_fallback(self):
        """Test fallback to bundled binary when system stockfish not available"""
        with patch('shutil.which') as mock_which:
            mock_which.return_value = None
            with patch.dict(os.environ, {}, clear=True):
                with patch('os.path.exists') as mock_exists:
                    mock_exists.return_value = True
                    path = get_engine_path()
                    self.assertIn('stockfish', path)
                    self.assertTrue(path.endswith(('linux', 'windows.exe', 'mac')))


if __name__ == '__main__':
    unittest.main()