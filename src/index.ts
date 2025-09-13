#!/usr/bin/env node

import { program } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import { Colors, Levels } from './utils/core';
import { Client } from './client/runner';
import { Color } from 'chess.js';

function getVersion(): string {
  const packagePath = path.join(__dirname, '..', 'package.json');
  try {
    const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
    return packageJson.version;
  } catch (error) {
    return '1.0.0';
  }
}

function main(): void {
  program
    .name('chs')
    .description('Play chess against the Stockfish engine in your terminal')
    .version(getVersion())
    .option('--play-black', 'Play the game with the black pieces')
    .option('--level <level>', 'Start a game with the given difficulty level (1-8)', '1')
    .helpOption('-h, --help', 'Display help for command');

  program
    .command('help', { isDefault: false })
    .description('Print all the possible usage information')
    .action(() => {
      console.log('Usage: chs [COMMAND] [FLAGS]\n');
      console.log('Valid values for [COMMAND]');
      console.log('  help         Print all the possible usage information');
      console.log('  version      Print the current version');
      console.log('\nValid values for [FLAGS]');
      console.log('  --play-black   Play the game with the black pieces');
      console.log('  --level=[LVL]  Start a game with the given difficulty level');
      console.log('\nValid values for [LVL]');
      console.log('  1     The least difficult setting');
      console.log('  2..7  Increasing difficulty');
      console.log('  8     The most difficult setting');
      console.log('');
      console.log('How to play: Your move: [MOVE]\n');
      console.log('Valid values for [MOVE]:');
      console.log('        Make moves using valid algebraic notation (e.g. Nf3, e4, etc.)');
      console.log('  back  Take back your last move');
      console.log('  hint  Get a hint from the engine');
      console.log('');
      console.log('Environment Variables:');
      console.log('  CHS_STOCKFISH_PATH   Override Stockfish engine path');
      console.log('');
      console.log('For Termux users: Install with "pkg install stockfish && npm install -g chs"');
      console.log('See TERMUX.md for detailed Termux installation and usage instructions.');
      console.log('');
    });

  program
    .command('version')
    .description('Print the current version')
    .action(() => {
      console.log(`Running chs ${Colors.BOLD}v${getVersion()}${Colors.RESET}\n`);
    });

  program.action((options) => {
    try {
      const level = Levels.levelOfInt(parseInt(options.level || '1', 10));
      const playAs: Color = options.playBlack ? 'b' : 'w';
      
      const client = new Client(level, playAs);
      client.run();
    } catch (error) {
      console.error(`${Colors.RED}\nUncaught error "${error?.constructor?.name || 'Error'}", exiting the app.\n${Colors.RESET}`);
      process.exit(1);
    }
  });

  program.parse();
}

if (require.main === module) {
  main();
}

export { main };