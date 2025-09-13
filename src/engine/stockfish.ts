import { spawn, ChildProcess } from 'child_process';
import * as os from 'os';
import * as path from 'path';
import * as fs from 'fs';
import { Levels } from '../utils/core';

export interface EngineMove {
  from: string;
  to: string;
  promotion?: string;
}

function isTermux(): boolean {
  return process.env.PREFIX === '/data/data/com.termux/files/usr' ||
         fs.existsSync('/data/data/com.termux/files/usr');
}

function getStockfishPath(): string {
  // Check environment variable first
  if (process.env.CHS_STOCKFISH_PATH) {
    return process.env.CHS_STOCKFISH_PATH;
  }

  // Check if we're in Termux
  if (isTermux()) {
    const termuxPaths = [
      '/data/data/com.termux/files/usr/bin/stockfish',
      '/system/bin/stockfish',
      'stockfish'
    ];
    
    for (const stockfishPath of termuxPaths) {
      if (fs.existsSync(stockfishPath)) {
        return stockfishPath;
      }
    }
    return 'stockfish'; // Fallback to PATH
  }

  // For regular systems, check bundled binaries
  const platform = os.platform();
  const arch = os.arch();
  
  const engineDir = path.join(__dirname, '..', '..', 'chs', 'engine');
  
  let binaryName: string;
  if (platform === 'linux') {
    if (arch === 'arm64' || arch === 'aarch64') {
      binaryName = 'stockfish_16_aarch64_linux';
    } else {
      binaryName = 'stockfish_10_x64_linux';
    }
  } else if (platform === 'darwin') {
    if (arch === 'arm64') {
      binaryName = 'stockfish_13_x64_mac'; // Use the same for now
    } else {
      binaryName = 'stockfish_13_x64_mac';
    }
  } else if (platform === 'win32') {
    binaryName = 'stockfish_10_x64_windows.exe';
  } else {
    // Fallback to system stockfish
    return 'stockfish';
  }

  const binaryPath = path.join(engineDir, binaryName);
  if (fs.existsSync(binaryPath)) {
    return binaryPath;
  }

  // Fallback to system stockfish
  return 'stockfish';
}

export class Engine {
  private process: ChildProcess | null = null;
  private level: number;
  private ready = false;
  private waitingForBestMove = false;
  private bestMoveCallback: ((move: string) => void) | null = null;

  constructor(level: number) {
    this.level = level;
  }

  async start(): Promise<void> {
    const stockfishPath = getStockfishPath();
    
    try {
      this.process = spawn(stockfishPath, [], {
        stdio: ['pipe', 'pipe', 'pipe']
      });

      this.process.on('error', (error) => {
        throw new Error(`Failed to start Stockfish: ${error.message}`);
      });

      this.process.stdout?.on('data', (data) => {
        const output = data.toString().trim();
        this.handleOutput(output);
      });

      this.process.stderr?.on('data', (data) => {
        console.error('Stockfish error:', data.toString());
      });

      await this.initializeEngine();
    } catch (error) {
      throw new Error(`Could not start Stockfish engine: ${error}`);
    }
  }

  private async initializeEngine(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!this.process?.stdin) {
        reject(new Error('Stockfish process not started'));
        return;
      }

      const timeout = setTimeout(() => {
        reject(new Error('Stockfish initialization timeout'));
      }, 5000);

      const readyHandler = (output: string) => {
        if (output.includes('uciok')) {
          clearTimeout(timeout);
          this.ready = true;
          resolve();
        }
      };

      const originalHandler = this.handleOutput.bind(this);
      this.handleOutput = (output: string) => {
        originalHandler(output);
        readyHandler(output);
      };

      this.send('uci');
      this.send(`setoption name Skill Level value ${Levels.value(this.level)}`);
      
      // Set single-threaded mode for Termux
      if (isTermux()) {
        this.send('setoption name Threads value 1');
      }
    });
  }

  private handleOutput(output: string): void {
    const lines = output.split('\n');
    
    for (const line of lines) {
      if (line.startsWith('bestmove')) {
        const parts = line.split(' ');
        const move = parts[1];
        
        if (this.waitingForBestMove && this.bestMoveCallback) {
          this.waitingForBestMove = false;
          this.bestMoveCallback(move);
          this.bestMoveCallback = null;
        }
      }
    }
  }

  private send(command: string): void {
    if (this.process?.stdin) {
      this.process.stdin.write(command + '\n');
    }
  }

  async getBestMove(fen: string): Promise<string> {
    if (!this.ready) {
      await this.start();
    }

    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error('Engine timeout'));
      }, 10000);

      this.bestMoveCallback = (move: string) => {
        clearTimeout(timeout);
        resolve(move);
      };

      this.waitingForBestMove = true;
      this.send(`position fen ${fen}`);
      this.send('go depth 15');
    });
  }

  quit(): void {
    if (this.process) {
      this.send('quit');
      this.process.kill();
      this.process = null;
    }
  }
}