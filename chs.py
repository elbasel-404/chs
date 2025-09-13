#!/usr/bin/env python

try:
    import chs.__main__
    chs.__main__.run()
except ImportError as e:
    if "python-chess" in str(e):
        # The helpful error message was already printed by the module
        exit(1)
    else:
        # Re-raise if it's a different ImportError
        raise
