import os
import platform
import math
import asyncio
import types

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

import chess.engine
from chs.utils.core import Levels


file_path = os.path.dirname(os.path.abspath(__file__))

if 'Windows' in platform.system():
  engine_path = 'stockfish_10_x64_windows.exe'
elif 'Linux' in platform.system():
  engine_path = 'stockfish_10_x64_linux'
else:
  engine_path = 'stockfish_13_x64_mac'

class Engine(object):
  def __init__(self, level):
    self.engine = chess.engine.SimpleEngine.popen_uci(os.path.join(file_path, engine_path))
    self.engine.configure({'Skill Level': Levels.value(level)})

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
