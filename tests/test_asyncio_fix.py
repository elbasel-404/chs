#!/usr/bin/env python3
"""
Test for asyncio.coroutine compatibility fix.
This test ensures that the monkey patch for asyncio.coroutine works correctly
with Python 3.11+ where the decorator was removed.
"""

import unittest
import sys


class TestAsyncioCoroutineFix(unittest.TestCase):
    
    def test_asyncio_coroutine_import(self):
        """Test that asyncio.coroutine is available after our compatibility fix."""
        # Import our stockfish module which contains the compatibility fix
        from chs.engine import stockfish
        import asyncio
        
        # Verify that asyncio.coroutine is now available
        self.assertTrue(hasattr(asyncio, 'coroutine'), 
                       "asyncio.coroutine should be available after compatibility fix")
        
    def test_chess_engine_import(self):
        """Test that chess.engine can be imported without AttributeError."""
        try:
            # This should not raise AttributeError about missing asyncio.coroutine
            import chess.engine
            self.assertTrue(True, "chess.engine imported successfully")
        except AttributeError as e:
            if "asyncio" in str(e) and "coroutine" in str(e):
                self.fail(f"asyncio.coroutine compatibility fix failed: {e}")
            else:
                # Re-raise if it's a different AttributeError
                raise
        except ImportError:
            # chess.engine not available is fine - we're only testing the compatibility fix
            self.skipTest("chess.engine not available (python-chess not installed)")
            
    def test_application_main_import(self):
        """Test that the main application can be imported without the asyncio error."""
        try:
            # This import chain is what was failing in the original error
            import chs.__main__
            self.assertTrue(True, "Main application imported successfully")
        except AttributeError as e:
            if "asyncio" in str(e) and "coroutine" in str(e):
                self.fail(f"asyncio.coroutine compatibility fix failed in main app: {e}")
            else:
                # Re-raise if it's a different AttributeError
                raise
        except ImportError as e:
            # Skip if dependencies are missing, we're only testing the compatibility fix
            if "chess" in str(e):
                self.skipTest("chess module not available")
            else:
                raise


if __name__ == '__main__':
    unittest.main()