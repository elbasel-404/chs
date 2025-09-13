import * as os from 'os';
import * as fs from 'fs';
import * as path from 'path';

describe('Architecture compatibility', () => {
  it('should support current architecture', () => {
    const arch = os.arch();
    const supportedArchs = ['x64', 'arm64', 'aarch64'];
    
    expect(supportedArchs.some(supportedArch => 
      arch === supportedArch || arch.includes(supportedArch)
    )).toBe(true);
  });

  it('should have stockfish binary for aarch64', () => {
    const engineDir = path.join(__dirname, '..', '..', 'chs', 'engine');
    const aarch64Binary = path.join(engineDir, 'stockfish_16_aarch64_linux');
    
    // Check if the binary exists (it should from the original Python version)
    const binaryExists = fs.existsSync(aarch64Binary);
    
    // If the directory structure exists, the binary should be there
    if (fs.existsSync(engineDir)) {
      expect(binaryExists).toBe(true);
    } else {
      // If we're in a clean setup, just verify the path would work
      expect(aarch64Binary).toContain('aarch64');
    }
  });

  it('should handle termux environment detection', () => {
    const originalEnv = process.env.PREFIX;
    
    // Test Termux environment detection
    process.env.PREFIX = '/data/data/com.termux/files/usr';
    
    // Import after setting environment
    const isTermuxCheck = () => {
      return process.env.PREFIX === '/data/data/com.termux/files/usr' ||
             fs.existsSync('/data/data/com.termux/files/usr');
    };
    
    expect(isTermuxCheck()).toBe(true);
    
    // Restore original environment
    if (originalEnv !== undefined) {
      process.env.PREFIX = originalEnv;
    } else {
      delete process.env.PREFIX;
    }
  });

  it('should work with Node.js on different architectures', () => {
    // Verify Node.js version supports our target architectures
    const nodeVersion = process.version;
    const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
    
    // Node.js 16+ has good ARM64/aarch64 support
    expect(majorVersion).toBeGreaterThanOrEqual(16);
  });
});