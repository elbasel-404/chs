# CHS for Termux

This document provides specific instructions for running CHS (terminal chess game) on Termux.

## What is Termux?

Termux is an Android terminal emulator that provides a Linux environment on Android devices. It runs on ARM/AArch64 architecture and has some differences from regular Linux distributions.

## Installation on Termux

### 1. Update Termux packages
```bash
pkg update && pkg upgrade
```

### 2. Install required packages
```bash
# Install Python
pkg install python

# Install Stockfish chess engine
pkg install stockfish
```

### 3. Install CHS
```bash
pip install chs
```

## Usage

Once installed, you can run CHS normally:
```bash
chs
```

## Troubleshooting

### Stockfish Engine Issues

If you encounter issues with the Stockfish engine, try:

1. **Verify Stockfish installation**:
   ```bash
   which stockfish
   stockfish quit
   ```

2. **Manual engine path** (if needed):
   ```bash
   export CHS_STOCKFISH_PATH=$(which stockfish)
   chs
   ```

3. **Alternative Stockfish installation**:
   ```bash
   pkg install clang
   # Then reinstall stockfish
   pkg reinstall stockfish
   ```

### Python Package Issues

If you have issues with Python packages:

```bash
pip install --upgrade pip
pip install --upgrade chs
```

### Memory Issues

On lower-end devices, you might want to use lower difficulty levels:
```bash
chs --level=1  # Easiest setting
```

## Technical Details

### Architecture Support

CHS has been modified to work on ARM/AArch64 architecture used by Android devices:

- Automatically detects Termux environment
- Uses system-installed Stockfish instead of bundled x86_64 binaries
- Provides helpful error messages for missing dependencies

### Environment Detection

The app detects Termux by checking:
- `/data/data/com.termux` directory existence
- `PREFIX` environment variable containing `com.termux`

### Engine Resolution Priority

1. `CHS_STOCKFISH_PATH` environment variable
2. System-installed stockfish (`pkg install stockfish`)
3. Bundled binaries (fallback, may not work on ARM)

## Contributing

If you encounter Termux-specific issues, please report them with:
- Device architecture: `uname -m`
- Termux version: `termux-info`
- Error messages and logs

## See Also

- [Main README](README.md) - General installation and usage
- [Termux Wiki](https://wiki.termux.com/) - Termux documentation