#!/usr/bin/env python3
"""
Demonstration script for CHS Termux compatibility features.
This script shows the key improvements made for Termux support.
"""

import os
import platform
from chs.engine.stockfish import is_termux, get_system_stockfish, get_engine_path


def main():
    print("=" * 60)
    print("CHS Termux Compatibility Demo")
    print("=" * 60)
    
    print("\n1. System Information:")
    print(f"   Platform: {platform.system()} {platform.machine()}")
    print(f"   Python: {platform.python_version()}")
    
    print("\n2. Termux Detection:")
    print(f"   Is Termux: {is_termux()}")
    if is_termux():
        print("   ✓ Termux environment detected")
    else:
        print("   ℹ Running on standard Linux/Unix system")
    
    print("\n3. Stockfish Engine Detection:")
    system_stockfish = get_system_stockfish()
    if system_stockfish:
        print(f"   ✓ System Stockfish found: {system_stockfish}")
    else:
        print("   ✗ No system Stockfish found")
    
    print(f"   Selected engine path: {get_engine_path()}")
    
    print("\n4. Environment Variable Override:")
    original_path = get_engine_path()
    print(f"   Default path: {original_path}")
    
    # Test environment variable override
    test_path = "/custom/stockfish/path"
    os.environ['CHS_STOCKFISH_PATH'] = test_path
    override_path = get_engine_path()
    
    if test_path in override_path:
        print(f"   ✓ Environment override working (would use: {test_path})")
    else:
        print(f"   ℹ Environment override fallback: {override_path}")
    
    # Clean up
    del os.environ['CHS_STOCKFISH_PATH']
    
    print("\n5. Installation Instructions:")
    if is_termux():
        print("   Termux installation:")
        print("   $ pkg update && pkg install python stockfish")
        print("   $ pip install chs")
    else:
        print("   Standard Linux installation:")
        print("   $ sudo apt install stockfish  # or equivalent")
        print("   $ pip install chs")
    
    print("\n6. Key Improvements for Termux:")
    print("   ✓ ARM/AArch64 architecture support")
    print("   ✓ Automatic system Stockfish detection")
    print("   ✓ Termux environment detection")
    print("   ✓ Helpful error messages with installation hints")
    print("   ✓ Environment variable override capability")
    print("   ✓ Comprehensive documentation (TERMUX.md)")
    
    print("\n" + "=" * 60)
    print("Demo completed! The project is now Termux-compatible.")
    print("=" * 60)


if __name__ == "__main__":
    main()