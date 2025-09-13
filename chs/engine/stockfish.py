import os
import platform
import math
import asyncio
import types
import shutil
import subprocess

# Fix for Python 3.11+ compatibility with older python-chess versions
# The asyncio.coroutine decorator was removed in Python 3.11+
if not hasattr(asyncio, 'coroutine'):
    def coroutine(func):
        """Compatibility wrapper for the removed asyncio.coroutine decorator"""
        # Convert generator function to coroutine function
        if asyncio.iscoroutinefunction(func):
            return func
        else:
            # For generator functions, create a coroutine wrapper
            async def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if hasattr(result, '__next__'):  # It's a generator
                    # Convert generator to async generator behavior
                    try:
                        value = None
                        while True:
                            value = result.send(value)
                            if hasattr(value, '__await__'):
                                value = await value
                    except StopIteration as e:
                        return e.value if hasattr(e, 'value') else None
                else:
                    return result
            return wrapper
    asyncio.coroutine = coroutine

try:
    import chess.engine
except ImportError:
    import sys
    print("Error: Missing required dependency 'python-chess'.", file=sys.stderr)
    print("Please install dependencies with:", file=sys.stderr)
    print("  pip install -r requirements.txt", file=sys.stderr)
    print("Or install the package with:", file=sys.stderr)
    print("  pip install python-chess", file=sys.stderr)
    raise ImportError("Missing required dependency 'python-chess'. Please install with: pip install python-chess")

from chs.utils.core import Levels


def is_termux():
    """Check if running in Termux environment"""
    # Check for Termux data directories (including beta and nightly versions)
    termux_paths = [
        '/data/data/com.termux',
        '/data/data/com.termux.beta', 
        '/data/data/com.termux.nightly'
    ]
    
    if any(os.path.exists(path) for path in termux_paths):
        return True
    
    # Check PREFIX environment variable for Termux patterns
    prefix = os.environ.get('PREFIX', '')
    return 'com.termux' in prefix

def get_system_stockfish():
    """Try to find system-installed stockfish"""
    return shutil.which('stockfish')

def get_engine_path():
    """Get the appropriate Stockfish engine path based on platform"""
    file_path = os.path.dirname(os.path.abspath(__file__))
    
    # Allow environment variable override (highest priority)
    env_engine = os.environ.get('CHS_STOCKFISH_PATH')
    if env_engine and os.path.exists(env_engine):
        return env_engine
    
    # Check for system stockfish first (better for Termux and other environments)
    system_stockfish = get_system_stockfish()
    if system_stockfish:
        return system_stockfish
    
    # Platform-specific bundled binaries as fallback
    system = platform.system()
    machine = platform.machine()
    
    if system == 'Windows':
        engine_path = 'stockfish_10_x64_windows.exe'
    elif system == 'Linux':
        # Check for ARM64/aarch64 architecture
        if machine in ('aarch64', 'arm64'):
            # Use ARM64-optimized binary
            engine_path = 'stockfish_16_aarch64_linux'
        elif machine.startswith(('arm', 'armv7l', 'armv8l')):
            # For other ARM variants, prefer system stockfish but fall back to ARM64 binary
            if system_stockfish:
                return system_stockfish
            # ARM64 binary might work on some ARM systems
            engine_path = 'stockfish_16_aarch64_linux'
        else:
            # Use x86-64 binary for x86_64 systems
            engine_path = 'stockfish_10_x64_linux'
    elif system == 'Darwin':  # macOS
        engine_path = 'stockfish_13_x64_mac'
    else:
        # Unknown platform, try system stockfish first
        if system_stockfish:
            return system_stockfish
        # Last resort fallback to x86-64 Linux binary
        engine_path = 'stockfish_10_x64_linux'
    
    bundled_path = os.path.join(file_path, engine_path)
    if os.path.exists(bundled_path):
        return bundled_path
    
    # If bundled binary doesn't exist, fall back to system stockfish
    if system_stockfish:
        return system_stockfish
        
    # If nothing works, return the expected path (will fail gracefully later)
    return bundled_path

class Engine(object):
  def __init__(self, level):
    engine_path = get_engine_path()
    try:
      self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
      skill_level = Levels.value(level)
      
      # Configure engine with appropriate settings
      engine_config = {'Skill Level': skill_level}
      
      # For mobile/ARM devices, add memory-friendly settings
      if is_termux() or platform.machine().startswith(('arm', 'aarch')):
          # Reduce memory usage for mobile devices
          engine_config.update({
              'Hash': 16,  # Reduce hash table size (MB)
              'Threads': 1,  # Use single thread on mobile
          })
      
      self.engine.configure(engine_config)
      
    except Exception as e:
      error_msg = f"Failed to start Stockfish engine at '{engine_path}'"
      
      if is_termux():
        error_msg += "\n\nFor Termux, please install Stockfish:"
        error_msg += "\n  pkg update && pkg install stockfish"
        error_msg += "\n\nIf you have installation issues, try:"
        error_msg += "\n  pkg install clang && pkg reinstall stockfish"
        error_msg += "\n\nAlternatively, set custom path:"
        error_msg += "\n  export CHS_STOCKFISH_PATH=/path/to/your/stockfish"
      elif not get_system_stockfish():
        error_msg += "\n\nPlease install Stockfish:"
        error_msg += "\n  - Ubuntu/Debian: apt install stockfish"
        error_msg += "\n  - Fedora: dnf install stockfish"
        error_msg += "\n  - Arch: pacman -S stockfish" 
        error_msg += "\n  - macOS: brew install stockfish"
        error_msg += "\n  - Windows: Download from https://stockfishchess.org/download/"
      
      raise RuntimeError(error_msg) from e

  def play(self, board, time=1.500):
    return self.engine.play(board, chess.engine.Limit(time=time))

  def score(self, board, pov=chess.WHITE):
    try:
      info = self.engine.analyse(board, chess.engine.Limit(time=0.500))
      cp = chess.engine.PovScore(info['score'], pov).pov(pov).relative.score()
      return cp
    except chess.engine.EngineTerminatedError:
      return None

  def normalize(self, cp):
    if cp is None:
      return None
    # https://github.com/ornicar/lila/blob/80646821b238d044aed5baf9efb7201cd4793b8b/ui/ceval/src/winningChances.ts#L10
    raw_score = 2 / (1 + math.exp(-0.004 * cp)) - 1
    return round(raw_score, 3)

  def done(self):
    try:
      return self.engine.quit()
    except chess.engine.EngineTerminatedError:
      return None
