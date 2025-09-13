import { Chess, Color, Square, Move } from 'chess.js';
import * as readline from 'readline';
const levenshtein = require('fast-levenshtein');
import { Engine } from '../engine/stockfish';
import { Board } from '../ui/board';
import { Colors } from '../utils/core';

export class GameOverException extends Error {}
export class WhiteWinsException extends GameOverException {}
export class BlackWinsException extends GameOverException {}
export class DrawException extends GameOverException {}
export class ResignException extends GameOverException {}

export class Client {
  private static readonly BACK = 'back';
  private static readonly HINT = 'hint';

  private uiBoard: Board;
  private playerColor: Color;
  private chess: Chess;
  private engine: Engine;
  private hintEngine: Engine;
  private rl: readline.Interface;
  private moveHistory: string[] = [];

  constructor(level: number, playerColor: Color) {
    this.uiBoard = new Board(level, playerColor);
    this.playerColor = playerColor;
    this.chess = new Chess();
    this.engine = new Engine(level);
    this.hintEngine = new Engine(8); // Max difficulty for hints
    
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
  }

  async run(): Promise<void> {
    try {
      console.log(`${Colors.GREEN}${Colors.BOLD}Welcome to CHS - Terminal Chess!${Colors.RESET}`);
      console.log(`${Colors.GRAY}Playing as ${this.playerColor === 'w' ? 'White' : 'Black'}${Colors.RESET}`);
      console.log('');

      await this.engine.start();
      await this.hintEngine.start();

      while (!this.chess.isGameOver()) {
        this.displayBoard();
        
        if (this.isPlayerTurn()) {
          await this.makePlayerMove();
        } else {
          await this.makeComputerMove();
        }
      }

      this.handleGameOver();
    } catch (error) {
      if (error instanceof GameOverException) {
        this.handleGameOver();
      } else {
        throw error;
      }
    } finally {
      this.engine.quit();
      this.hintEngine.quit();
      this.rl.close();
    }
  }

  private displayBoard(): void {
    this.uiBoard.display(this.chess);
    this.uiBoard.displayGameInfo(this.chess);
  }

  private isPlayerTurn(): boolean {
    return this.chess.turn() === this.playerColor;
  }

  private async makePlayerMove(): Promise<void> {
    return new Promise((resolve, reject) => {
      const prompt = `${Colors.BOLD}Your move: ${Colors.RESET}`;
      
      this.rl.question(prompt, async (input) => {
        try {
          const move = input.trim().toLowerCase();
          
          if (move === Client.BACK) {
            this.takeBackMove();
            resolve();
            return;
          }
          
          if (move === Client.HINT) {
            await this.showHint();
            resolve();
            return;
          }
          
          if (this.isValidMove(move)) {
            const moveObj = this.chess.move(move);
            if (moveObj) {
              this.uiBoard.setLastMove(moveObj.from, moveObj.to);
              this.moveHistory.push(moveObj.san);
              resolve();
            } else {
              this.uiBoard.displayError('Invalid move. Try again.');
              await this.makePlayerMove();
              resolve();
            }
          } else {
            const suggestion = this.getSuggestion(move);
            if (suggestion) {
              this.uiBoard.displayError(`Invalid move. Did you mean "${suggestion}"?`);
            } else {
              this.uiBoard.displayError('Invalid move. Use algebraic notation (e.g., e4, Nf3).');
            }
            await this.makePlayerMove();
            resolve();
          }
        } catch (error) {
          reject(error);
        }
      });
    });
  }

  private async makeComputerMove(): Promise<void> {
    this.uiBoard.displayThinking();
    
    try {
      const bestMove = await this.engine.getBestMove(this.chess.fen());
      
      if (bestMove && bestMove !== '(none)') {
        const moveObj = this.chess.move(bestMove);
        if (moveObj) {
          this.uiBoard.setLastMove(moveObj.from, moveObj.to);
          this.moveHistory.push(moveObj.san);
          console.log(`${Colors.GRAY}Computer plays: ${moveObj.san}${Colors.RESET}`);
        }
      }
    } catch (error) {
      console.error(`${Colors.RED}Engine error: ${error}${Colors.RESET}`);
    }
  }

  private takeBackMove(): void {
    if (this.moveHistory.length >= 2) {
      // Take back both player and computer moves
      this.chess.undo();
      this.chess.undo();
      this.moveHistory.pop();
      this.moveHistory.pop();
      console.log(`${Colors.YELLOW}Took back last move.${Colors.RESET}`);
    } else if (this.moveHistory.length === 1) {
      // Only take back player move if computer hasn't moved yet
      this.chess.undo();
      this.moveHistory.pop();
      console.log(`${Colors.YELLOW}Took back last move.${Colors.RESET}`);
    } else {
      console.log(`${Colors.RED}No moves to take back.${Colors.RESET}`);
    }
  }

  private async showHint(): Promise<void> {
    try {
      console.log(`${Colors.GRAY}Analyzing position...${Colors.RESET}`);
      const bestMove = await this.hintEngine.getBestMove(this.chess.fen());
      
      if (bestMove && bestMove !== '(none)') {
        // Convert UCI notation to SAN for display
        const tempChess = new Chess(this.chess.fen());
        const moveObj = tempChess.move(bestMove);
        if (moveObj) {
          this.uiBoard.displayHint(moveObj.san);
        } else {
          this.uiBoard.displayHint(bestMove);
        }
      } else {
        console.log(`${Colors.YELLOW}No hint available.${Colors.RESET}`);
      }
    } catch (error) {
      console.log(`${Colors.RED}Could not get hint: ${error}${Colors.RESET}`);
    }
  }

  private isValidMove(move: string): boolean {
    try {
      const tempChess = new Chess(this.chess.fen());
      const result = tempChess.move(move);
      return result !== null;
    } catch {
      return false;
    }
  }

  private getSuggestion(invalidMove: string): string | null {
    const legalMoves = this.chess.moves();
    let bestMatch: string | null = null;
    let bestDistance = Infinity;

    for (const legalMove of legalMoves) {
      const distance = levenshtein.get(invalidMove.toLowerCase(), legalMove.toLowerCase());
      if (distance < bestDistance && distance <= 2) { // Only suggest if close enough
        bestDistance = distance;
        bestMatch = legalMove;
      }
    }

    return bestMatch;
  }

  private handleGameOver(): void {
    this.displayBoard();
    
    if (this.chess.isCheckmate()) {
      const winner = this.chess.turn() === 'w' ? 'Black' : 'White';
      console.log(`${Colors.GREEN}${Colors.BOLD}Checkmate! ${winner} wins!${Colors.RESET}`);
      
      if ((winner === 'White' && this.playerColor === 'w') || 
          (winner === 'Black' && this.playerColor === 'b')) {
        console.log(`${Colors.GREEN}Congratulations! You won!${Colors.RESET}`);
      } else {
        console.log(`${Colors.RED}Computer wins. Better luck next time!${Colors.RESET}`);
      }
    } else if (this.chess.isDraw()) {
      console.log(`${Colors.YELLOW}${Colors.BOLD}Game ended in a draw.${Colors.RESET}`);
      
      if (this.chess.isStalemate()) {
        console.log(`${Colors.GRAY}Stalemate${Colors.RESET}`);
      } else if (this.chess.isThreefoldRepetition()) {
        console.log(`${Colors.GRAY}Draw by threefold repetition${Colors.RESET}`);
      } else if (this.chess.isInsufficientMaterial()) {
        console.log(`${Colors.GRAY}Draw by insufficient material${Colors.RESET}`);
      }
    }
    
    console.log('');
    console.log('Thanks for playing CHS!');
  }
}