import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock, call
from chs.engine.stockfish import Engine, is_termux, get_system_stockfish, get_engine_path


class TestTermuxComprehensive(unittest.TestCase):
    """Comprehensive tests for Termux environment simulation and compatibility"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.mock_stockfish_path = os.path.join(self.temp_dir, 'stockfish')
        # Create a dummy stockfish executable
        with open(self.mock_stockfish_path, 'w') as f:
            f.write('#!/bin/bash\necho "Stockfish mock"')
        os.chmod(self.mock_stockfish_path, 0o755)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_termux_prefix_variations(self):
        """Test various Termux PREFIX environment variable patterns"""
        termux_prefixes = [
            '/data/data/com.termux/files/usr',
            '/data/data/com.termux.beta/files/usr', 
            '/data/data/com.termux.nightly/files/usr',
            '/data/data/com.termux/files/usr/',  # with trailing slash
        ]
        
        for prefix in termux_prefixes:
            with self.subTest(prefix=prefix):
                with patch.dict(os.environ, {'PREFIX': prefix}):
                    self.assertTrue(is_termux(), f"Failed to detect Termux with PREFIX: {prefix}")
    
    def test_termux_data_directory_variations(self):
        """Test Termux detection via various data directory paths"""
        termux_dirs = [
            '/data/data/com.termux',
            '/data/data/com.termux.beta',
            '/data/data/com.termux.nightly',
        ]
        
        for termux_dir in termux_dirs:
            with self.subTest(termux_dir=termux_dir):
                with patch('os.path.exists') as mock_exists:
                    def exists_side_effect(path):
                        return path == termux_dir
                    mock_exists.side_effect = exists_side_effect
                    
                    # Clear environment to rely only on directory detection
                    with patch.dict(os.environ, {}, clear=True):
                        self.assertTrue(is_termux(), f"Failed to detect Termux with directory: {termux_dir}")
    
    @patch('platform.system')
    @patch('platform.machine')
    def test_arm_architecture_variations(self, mock_machine, mock_system):
        """Test ARM architecture detection with various machine types"""
        mock_system.return_value = 'Linux'
        
        arm_architectures = ['aarch64', 'armv7l', 'armv8l', 'arm64']
        
        for arch in arm_architectures:
            with self.subTest(arch=arch):
                mock_machine.return_value = arch
                
                with patch('shutil.which') as mock_which:
                    mock_which.return_value = self.mock_stockfish_path
                    path = get_engine_path()
                    self.assertEqual(path, self.mock_stockfish_path, 
                                   f"Failed to detect system stockfish for ARM arch: {arch}")
    
    def test_termux_stockfish_paths(self):
        """Test various Termux Stockfish installation paths"""
        termux_stockfish_paths = [
            '/data/data/com.termux/files/usr/bin/stockfish',
            '/data/data/com.termux/files/usr/games/stockfish',
            '/system/bin/stockfish',
            '/usr/bin/stockfish',  # Common system path
            '/usr/games/stockfish',  # Ubuntu/Debian path
        ]
        
        for stockfish_path in termux_stockfish_paths:
            with self.subTest(stockfish_path=stockfish_path):
                with patch('shutil.which') as mock_which:
                    mock_which.return_value = stockfish_path
                    
                    detected_path = get_system_stockfish()
                    self.assertEqual(detected_path, stockfish_path, 
                                   f"Failed to detect Stockfish at: {stockfish_path}")
    
    def test_environment_variable_priority(self):
        """Test that CHS_STOCKFISH_PATH takes priority over system detection"""
        custom_path = '/custom/stockfish/path'
        system_path = '/usr/bin/stockfish'
        
        with patch.dict(os.environ, {'CHS_STOCKFISH_PATH': custom_path}):
            with patch('os.path.exists') as mock_exists:
                with patch('shutil.which') as mock_which:
                    mock_exists.return_value = True  # Custom path exists
                    mock_which.return_value = system_path  # System has stockfish too
                    
                    path = get_engine_path()
                    self.assertEqual(path, custom_path, 
                                   "Environment variable should take priority over system stockfish")
    
    def test_termux_engine_initialization_success(self):
        """Test successful engine initialization in simulated Termux environment"""
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            with patch('shutil.which') as mock_which:
                mock_which.return_value = self.mock_stockfish_path
                
                with patch('chess.engine.SimpleEngine.popen_uci') as mock_popen:
                    mock_engine = MagicMock()
                    mock_popen.return_value = mock_engine
                    
                    # This should succeed without throwing an exception
                    try:
                        engine = Engine(level=1)
                        self.assertIsNotNone(engine)
                        mock_popen.assert_called_once_with(self.mock_stockfish_path)
                    except Exception as e:
                        self.fail(f"Engine initialization failed in Termux environment: {e}")
    
    def test_termux_engine_initialization_failure(self):
        """Test proper error handling when Stockfish is not available in Termux"""
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            with patch('shutil.which') as mock_which:
                mock_which.return_value = None  # No system stockfish
                
                with patch('os.path.exists') as mock_exists:
                    mock_exists.return_value = False  # No bundled binary
                    
                    with patch('chess.engine.SimpleEngine.popen_uci') as mock_popen:
                        mock_popen.side_effect = Exception("No such file")
                        
                        with self.assertRaises(RuntimeError) as context:
                            Engine(level=1)
                        
                        error_msg = str(context.exception)
                        self.assertIn("Failed to start Stockfish engine", error_msg)
                        self.assertIn("pkg install stockfish", error_msg)
    
    def test_non_termux_environment_error_message(self):
        """Test error message for non-Termux environments when Stockfish is missing"""
        # Simulate non-Termux environment
        with patch.dict(os.environ, {}, clear=True):
            with patch('os.path.exists') as mock_exists:
                mock_exists.return_value = False
                
                with patch('shutil.which') as mock_which:
                    mock_which.return_value = None
                    
                    with patch('chess.engine.SimpleEngine.popen_uci') as mock_popen:
                        mock_popen.side_effect = Exception("No such file")
                        
                        with self.assertRaises(RuntimeError) as context:
                            Engine(level=1)
                        
                        error_msg = str(context.exception)
                        self.assertIn("Failed to start Stockfish engine", error_msg)
                        self.assertIn("apt install stockfish", error_msg)
                        self.assertNotIn("pkg install", error_msg)
    
    @patch('platform.system')
    def test_cross_platform_compatibility(self, mock_system):
        """Test that the engine works across different platforms"""
        platforms = ['Linux', 'Darwin', 'Windows']
        
        for platform in platforms:
            with self.subTest(platform=platform):
                mock_system.return_value = platform
                
                with patch('shutil.which') as mock_which:
                    mock_which.return_value = self.mock_stockfish_path
                    
                    path = get_engine_path()
                    self.assertIsNotNone(path, f"Failed to get engine path for platform: {platform}")
    
    def test_memory_constrained_environment(self):
        """Test behavior in memory-constrained environments like mobile devices"""
        # This test simulates lower memory scenarios that might occur on mobile
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            with patch('shutil.which') as mock_which:
                mock_which.return_value = self.mock_stockfish_path
                
                with patch('chess.engine.SimpleEngine.popen_uci') as mock_popen:
                    mock_engine = MagicMock()
                    mock_popen.return_value = mock_engine
                    
                    # Test with lowest difficulty level (memory-friendly)
                    engine = Engine(level=1)
                    
                    # Verify engine was configured for low skill level
                    mock_engine.configure.assert_called_once()
                    configure_args = mock_engine.configure.call_args[0][0]
                    self.assertIn('Skill Level', configure_args)
    
    def test_termux_path_resolution_order(self):
        """Test the order of path resolution in Termux environment"""
        custom_env_path = '/custom/env/stockfish'
        system_path = '/usr/bin/stockfish'
        bundled_path = '/bundled/stockfish'
        
        # Test 1: Environment variable should win
        with patch.dict(os.environ, {'CHS_STOCKFISH_PATH': custom_env_path}):
            with patch('os.path.exists') as mock_exists:
                mock_exists.return_value = True
                
                with patch('shutil.which') as mock_which:
                    mock_which.return_value = system_path
                    
                    path = get_engine_path()
                    self.assertEqual(path, custom_env_path)
        
        # Test 2: System path should win over bundled
        with patch.dict(os.environ, {}, clear=True):
            with patch('shutil.which') as mock_which:
                mock_which.return_value = system_path
                
                with patch('os.path.exists') as mock_exists:
                    mock_exists.return_value = True
                    
                    path = get_engine_path()
                    self.assertEqual(path, system_path)


if __name__ == '__main__':
    unittest.main()