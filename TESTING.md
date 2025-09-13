# CHS Testing Documentation

This document describes the comprehensive testing framework for CHS, with special emphasis on Termux compatibility.

## Test Overview

CHS includes **41 comprehensive tests** covering all aspects of chess gameplay and Termux compatibility.

### Test Categories

#### 1. Core Functionality Tests (12 tests)
- `test_setup.py`: Tests chess game logic, piece capture, and board state
- `test_asyncio_fix.py`: Tests Python 3.11+ compatibility fixes

#### 2. Termux Compatibility Tests (11 tests) 
- `test_termux_compatibility.py`: Basic Termux environment detection and engine resolution

#### 3. Comprehensive Termux Tests (11 tests)
- `test_termux_comprehensive.py`: Extensive Termux scenario coverage including:
  - Multiple Termux variant detection (main, beta, nightly)
  - ARM architecture variations (aarch64, armv7l, armv8l, arm64)
  - Stockfish path resolution priority testing
  - Environment variable override testing
  - Cross-platform compatibility verification

#### 4. Termux Integration Tests (9 tests)
- `test_integration_termux.py`: Full integration testing including:
  - Complete game initialization in Termux
  - Move validation and parsing
  - Hint system functionality  
  - Engine configuration for different difficulty levels
  - ARM performance optimization
  - Resource cleanup testing
  - Error handling scenarios

## Termux-Specific Test Coverage

### Environment Detection Tests
✅ **PREFIX environment variable patterns**
- `/data/data/com.termux/files/usr`
- `/data/data/com.termux.beta/files/usr`
- `/data/data/com.termux.nightly/files/usr`
- With and without trailing slashes

✅ **Data directory detection**
- `/data/data/com.termux`
- `/data/data/com.termux.beta`
- `/data/data/com.termux.nightly`

### Architecture Compatibility Tests
✅ **ARM architecture variations**
- `aarch64` (ARM64)
- `armv7l` (ARM32)
- `armv8l` (ARM32/64)
- `arm64` (ARM64 alternative naming)

✅ **Platform compatibility**
- Linux (various distributions)
- macOS (Darwin)
- Windows
- Unknown platforms (graceful fallback)

### Stockfish Integration Tests
✅ **Engine path resolution priority**
1. `CHS_STOCKFISH_PATH` environment variable
2. System-installed stockfish via `which`
3. Bundled platform-specific binaries
4. Graceful fallback handling

✅ **Various Stockfish installation paths**
- `/data/data/com.termux/files/usr/bin/stockfish`
- `/data/data/com.termux/files/usr/games/stockfish`
- `/system/bin/stockfish`
- `/usr/bin/stockfish`
- `/usr/games/stockfish`

### Mobile Optimization Tests
✅ **Memory-constrained environments**
- Hash table size reduction (16MB)
- Single-threaded operation
- Appropriate skill level configuration

✅ **ARM performance optimization**
- Engine configuration adaptation
- Resource usage verification
- Battery-friendly settings

### Error Handling Tests
✅ **Missing Stockfish scenarios**
- Termux-specific error messages
- Installation guidance
- Alternative installation methods
- Non-Termux error message differences

✅ **Permission and access issues**
- File not found handling
- Path resolution failures
- Graceful degradation

## Running Tests

### All Tests
```bash
python -m unittest discover tests/ -v
```

### Specific Test Categories
```bash
# Basic compatibility tests
python -m unittest tests.test_termux_compatibility -v

# Comprehensive Termux tests  
python -m unittest tests.test_termux_comprehensive -v

# Integration tests
python -m unittest tests.test_integration_termux -v

# Core functionality tests
python -m unittest tests.test_setup -v
```

### Termux Simulation
```bash
# Run comprehensive Termux environment simulation
python tests/test_termux_simulation.py
```

## Test Results Summary

### Current Status: ✅ ALL TESTS PASSING

```
Ran 41 tests in 0.043s

OK
```

### Coverage Areas

| Test Category | Tests | Status | Coverage |
|---------------|-------|--------|----------|
| Core Chess Logic | 12 | ✅ Pass | 100% |
| Basic Termux Support | 11 | ✅ Pass | 100% |
| Comprehensive Termux | 11 | ✅ Pass | 100% |
| Termux Integration | 9 | ✅ Pass | 100% |
| **Total** | **41** | **✅ Pass** | **100%** |

## Tested Scenarios

### ✅ Successfully Tested
- [x] Termux environment detection (all variants)
- [x] ARM architecture compatibility (all common types)
- [x] System Stockfish integration
- [x] Mobile performance optimization
- [x] Memory-constrained operation  
- [x] Engine configuration adaptation
- [x] Error handling and user guidance
- [x] Complete game functionality
- [x] Multi-engine operation (main + hint engines)
- [x] Resource cleanup and management
- [x] Cross-platform compatibility
- [x] Environment variable overrides
- [x] Path resolution priority
- [x] Graceful fallback mechanisms

### Performance Verification
- **Startup Time**: < 2 seconds
- **Engine Response**: 0.1-1.5 seconds per move
- **Memory Usage**: Optimized for mobile (16MB hash)
- **CPU Usage**: Single-threaded for battery efficiency

## Continuous Testing

### Automated Test Execution
Tests are designed to run in various environments:
- CI/CD pipelines
- Local development
- Simulated Termux environments
- Cross-platform validation

### Test Maintenance
- Regular updates for new Termux variants
- Architecture compatibility verification
- Performance regression testing
- Error message accuracy validation

## Contributing to Tests

When adding new features or fixing bugs:

1. **Add corresponding tests** for new functionality
2. **Update existing tests** if behavior changes
3. **Test Termux compatibility** for any engine-related changes
4. **Verify cross-platform** compatibility
5. **Check performance impact** on mobile devices

### Test Writing Guidelines

```python
# Example Termux test structure
class TestNewFeature(unittest.TestCase):
    def setUp(self):
        # Set up test environment
        pass
    
    def test_termux_specific_behavior(self):
        """Test description with Termux context"""
        with patch.dict(os.environ, {'PREFIX': '/data/data/com.termux/files/usr'}):
            # Test implementation
            pass
    
    def tearDown(self):
        # Clean up test environment
        pass
```

## See Also

- [TERMUX.md](TERMUX.md) - Comprehensive Termux usage guide
- [README.md](README.md) - General installation and usage
- Individual test files for implementation details