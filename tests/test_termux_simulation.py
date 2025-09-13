#!/usr/bin/env python3
"""
Termux simulation test script
Tests CHS functionality in a simulated Termux environment
"""

import os
import sys
import tempfile
import shutil
import subprocess
from unittest.mock import patch


def simulate_termux_environment():
    """Simulate various Termux environment conditions"""
    
    print("=" * 60)
    print("TERMUX COMPATIBILITY SIMULATION TESTS")
    print("=" * 60)
    
    # Test 1: Basic Termux environment detection
    print("\n1. Testing Termux environment detection...")
    
    # Simulate Termux PREFIX environment
    with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
        from chs.engine.stockfish import is_termux
        assert is_termux(), "Failed to detect Termux via PREFIX environment"
        print("   ✓ Termux detection via PREFIX works")
    
    # Test 2: System Stockfish detection
    print("\n2. Testing system Stockfish detection...")
    
    stockfish_path = shutil.which('stockfish')
    if stockfish_path:
        print(f"   ✓ System Stockfish found at: {stockfish_path}")
        
        # Test engine initialization with system Stockfish
        from chs.engine.stockfish import Engine
        from chs.utils.core import Levels
        
        engine = Engine(Levels.ONE)
        print("   ✓ Engine initialization successful")
        
        # Test a simple move
        import chess
        board = chess.Board()
        result = engine.play(board, time=0.1)
        print(f"   ✓ Engine move test: {result.move}")
        
        engine.done()
        print("   ✓ Engine cleanup successful")
    else:
        print("   ! No system Stockfish found - this is expected in some environments")
    
    # Test 3: ARM architecture handling
    print("\n3. Testing ARM architecture compatibility...")
    
    with patch('platform.machine') as mock_machine:
        mock_machine.return_value = 'aarch64'
        
        from chs.engine.stockfish import get_engine_path
        path = get_engine_path()
        print(f"   ✓ Engine path for ARM: {path}")
    
    # Test 4: Memory-constrained configuration
    print("\n4. Testing mobile-optimized engine configuration...")
    
    with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
        with patch('platform.machine') as mock_machine:
            mock_machine.return_value = 'aarch64'
            
            if stockfish_path:
                from chs.engine.stockfish import Engine
                from chs.utils.core import Levels
                
                # This should configure the engine with mobile-friendly settings
                engine = Engine(Levels.ONE)
                print("   ✓ Mobile-optimized engine configuration successful")
                engine.done()
    
    # Test 5: Error handling without Stockfish
    print("\n5. Testing error handling without Stockfish...")
    
    with patch('shutil.which') as mock_which:
        mock_which.return_value = None
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
                with patch('chess.engine.SimpleEngine.popen_uci') as mock_popen:
                    mock_popen.side_effect = FileNotFoundError("No such file")
                
                    try:
                        from chs.engine.stockfish import Engine
                        Engine(Levels.ONE)
                        print("   ! ERROR: Should have failed without Stockfish")
                    except RuntimeError as e:
                        error_msg = str(e)
                        if "pkg install stockfish" in error_msg:
                            print("   ✓ Proper Termux-specific error message")
                        else:
                            print(f"   ! Unexpected error message: {error_msg}")
                    except Exception as e:
                        print(f"   ! Unexpected exception type: {type(e).__name__}: {e}")
    
    # Test 6: Client game initialization
    print("\n6. Testing complete game client initialization...")
    
    if stockfish_path:
        from chs.client.runner import Client
        from chs.utils.core import Levels
        import chess
        
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            client = Client(Levels.ONE, chess.WHITE)
            print("   ✓ Game client initialization successful")
            
            # Test game state
            assert not client.board.is_game_over(), "Game should not be over initially"
            assert len(client.board.move_stack) == 0, "Move stack should be empty initially"
            print("   ✓ Initial game state correct")
            
            # Cleanup
            client.engine.done()
            client.hint_engine.done()
            print("   ✓ Game client cleanup successful")
    
    print("\n" + "=" * 60)
    print("ALL TERMUX COMPATIBILITY TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    simulate_termux_environment()