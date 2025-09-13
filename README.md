# ♗ chs

> Play chess against the Stockfish engine in your terminal.

<img src="https://travis-ci.org/nickzuber/chs.svg?branch=master" /> <img src="https://img.shields.io/badge/project-active-brightgreen.svg" /> <img src="https://img.shields.io/badge/status-stable-brightgreen.svg" /> <img src="https://img.shields.io/pypi/dm/chs.svg?color=yellow" /> <img src="https://img.shields.io/pypi/format/chs.svg" /> <img src="https://img.shields.io/badge/state-released-brightgreen.svg" /> <img src="https://img.shields.io/badge/license-MIT%20Licence-blue.svg" />

<img src="https://user-images.githubusercontent.com/10540865/119232802-80c34700-baf4-11eb-9fed-af558575ae4e.png" />

### Table of Contents

- [Installation](#installation)
  - [Pip](#pip)
  - [Arch Linux](#arch-linux)
- [Usage](#usage)
  - [How to start playing](#how-to-start-playing)
  - [How to play](#how-to-play)
- [License](#license)

## Installation

#### Termux (Android)

CHS has comprehensive Termux support with extensive testing and mobile optimizations:

```bash
# Install Python and pip
pkg install python

# Install Stockfish engine  
pkg install stockfish

# Install chs
pip install chs
```

**Termux Features:**
- ✅ **Full ARM/AArch64 support** - Works on all Android architectures
- ✅ **Mobile optimizations** - Reduced memory usage and single-threading for battery life
- ✅ **Multi-variant support** - Works with Termux, Termux Beta, and Termux Nightly
- ✅ **Comprehensive testing** - 41 tests covering all Termux scenarios
- ✅ **Smart error handling** - Detailed troubleshooting guidance for mobile devices

For detailed Termux instructions and troubleshooting, see [TERMUX.md](TERMUX.md).

#### Pip

This package is available via PyPi.

```
$ python3 -m pip install chs
```

**Note**: On some systems, you may also need to install the Stockfish chess engine separately:
- **Ubuntu/Debian**: `sudo apt install stockfish`
- **Fedora**: `sudo dnf install stockfish`  
- **Arch Linux**: `sudo pacman -S stockfish`
- **macOS**: `brew install stockfish`

#### Arch Linux

There is a [chs-git](https://aur.archlinux.org/packages/chs-git/) package in the Arch User Repository, which you can install with an AUR helper:

```
$ yay -S chs-git || paru -S chs-git
```

## Usage

To play against the default level 1 (easiest) version of the Stockfish engine, just run `chs` command.

### How to start playing

```
$ chs
```

To see all possible options, use the help command.

```
$ chs help
```

To play as the black pieces, use the `--play-black` flag.

```
$ chs --play-black
```

You can also specify the level of the engine if you want to tweak the difficulty.

```
$ chs --level=8
```

#### Termux-specific Usage

On Termux, the app will automatically detect the environment and use the system-installed Stockfish. If you encounter any issues, you can manually specify the Stockfish path:

```bash
export CHS_STOCKFISH_PATH=/data/data/com.termux/files/usr/bin/stockfish
chs
```

### How to play

There are a few things you can do while playing:

- Make moves using valid algebraic notation (e.g. `Nf3`, `e4`, etc.).
- Take back your last move by playing `back` instead of a valid move.
- Get a hint from the engine by playing `hint` instead of a valid move.

## License

This software is free to use under the MIT License. See [this reference](https://opensource.org/licenses/MIT) for license text and copyright information.
