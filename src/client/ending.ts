import { Chess } from 'chess.js';
import { Colors } from '../utils/core';

export class GameOver {
  static checkGameState(chess: Chess): void {
    if (chess.isGameOver()) {
      if (chess.isCheckmate()) {
        const winner = chess.turn() === 'w' ? 'Black' : 'White';
        console.log(`${Colors.GREEN}${Colors.BOLD}Checkmate! ${winner} wins!${Colors.RESET}`);
      } else if (chess.isDraw()) {
        console.log(`${Colors.YELLOW}${Colors.BOLD}Game ended in a draw.${Colors.RESET}`);
        
        if (chess.isStalemate()) {
          console.log(`${Colors.GRAY}Reason: Stalemate${Colors.RESET}`);
        } else if (chess.isThreefoldRepetition()) {
          console.log(`${Colors.GRAY}Reason: Threefold repetition${Colors.RESET}`);
        } else if (chess.isInsufficientMaterial()) {
          console.log(`${Colors.GRAY}Reason: Insufficient material${Colors.RESET}`);
        } else {
          console.log(`${Colors.GRAY}Reason: 50-move rule${Colors.RESET}`);
        }
      }
    }
  }

  static isGameOver(chess: Chess): boolean {
    return chess.isGameOver();
  }

  static getWinner(chess: Chess): 'white' | 'black' | 'draw' | null {
    if (!chess.isGameOver()) {
      return null;
    }

    if (chess.isDraw()) {
      return 'draw';
    }

    if (chess.isCheckmate()) {
      // The player whose turn it is has been checkmated
      return chess.turn() === 'w' ? 'black' : 'white';
    }

    return 'draw'; // Fallback
  }
}