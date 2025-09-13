import { Chess, Color, Square } from 'chess.js';
import { Colors, Styles } from '../utils/core';

const PIECE_SYMBOLS: { [key: string]: string } = {
  'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
  'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
};

export class Board {
  private level: number;
  private playerColor: Color;
  private lastMove: { from: Square; to: Square } | null = null;

  constructor(level: number, playerColor: Color) {
    this.level = level;
    this.playerColor = playerColor;
  }

  setLastMove(from: Square, to: Square): void {
    this.lastMove = { from, to };
  }

  display(chess: Chess): void {
    const board = chess.board();
    const isFlipped = this.playerColor === 'b';
    
    console.log('');
    this.printColumnHeaders(isFlipped);
    this.printTopBorder();
    
    for (let rank = 0; rank < 8; rank++) {
      const displayRank = isFlipped ? rank : 7 - rank;
      const actualRank = isFlipped ? 8 - rank : rank + 1;
      
      let line = `${Colors.GRAY} ${actualRank} ${Colors.RESET}│`;
      
      for (let file = 0; file < 8; file++) {
        const displayFile = isFlipped ? 7 - file : file;
        const square = board[displayRank][displayFile];
        const squareName = `${'abcdefgh'[displayFile]}${8 - displayRank}` as Square;
        
        const isLightSquare = (displayRank + displayFile) % 2 === 1;
        const isLastMoveSquare = this.lastMove && 
          (this.lastMove.from === squareName || this.lastMove.to === squareName);
        
        let bgColor: string;
        if (isLastMoveSquare) {
          bgColor = isLightSquare ? Colors.Backgrounds.GREEN_LIGHT : Colors.Backgrounds.GREEN_DARK;
        } else {
          bgColor = isLightSquare ? Colors.Backgrounds.LIGHT : Colors.Backgrounds.DARK;
        }
        
        let piece = ' ';
        let pieceColor = Colors.WHITE;
        
        if (square) {
          const pieceKey = square.color === 'w' ? square.type.toUpperCase() : square.type.toLowerCase();
          piece = PIECE_SYMBOLS[pieceKey] || square.type;
          pieceColor = square.color === 'w' ? Colors.WHITE : Colors.DARK;
        }
        
        line += `${bgColor}${pieceColor} ${piece} ${Colors.RESET}`;
      }
      
      line += `│${Colors.GRAY} ${actualRank} ${Colors.RESET}`;
      console.log(line);
    }
    
    this.printBottomBorder();
    this.printColumnHeaders(isFlipped);
    console.log('');
  }

  private printColumnHeaders(isFlipped: boolean): void {
    const files = isFlipped ? 'hgfedcba' : 'abcdefgh';
    let header = `${Colors.GRAY}   `;
    for (const file of files) {
      header += ` ${file} `;
    }
    header += `   ${Colors.RESET}`;
    console.log(header);
  }

  private printTopBorder(): void {
    console.log(`${Colors.GRAY}   ┌${'───'.repeat(8)}┐   ${Colors.RESET}`);
  }

  private printBottomBorder(): void {
    console.log(`${Colors.GRAY}   └${'───'.repeat(8)}┘   ${Colors.RESET}`);
  }

  displayGameInfo(chess: Chess): void {
    const turn = chess.turn() === 'w' ? 'White' : 'Black';
    const playerTurn = chess.turn() === this.playerColor ? 'Your' : 'Computer\'s';
    
    console.log(`${Colors.BOLD}${turn} to move (${playerTurn} turn)${Colors.RESET}`);
    
    if (chess.isCheck()) {
      console.log(`${Colors.RED}${Colors.BOLD}Check!${Colors.RESET}`);
    }
    
    if (chess.isCheckmate()) {
      const winner = chess.turn() === 'w' ? 'Black' : 'White';
      console.log(`${Colors.GREEN}${Colors.BOLD}Checkmate! ${winner} wins!${Colors.RESET}`);
    } else if (chess.isDraw()) {
      console.log(`${Colors.YELLOW}${Colors.BOLD}Draw!${Colors.RESET}`);
    }
    
    console.log('');
  }

  displayMovePrompt(): void {
    process.stdout.write(`${Colors.BOLD}Your move: ${Colors.RESET}`);
  }

  displayThinking(): void {
    console.log(`${Colors.GRAY}Computer is thinking...${Colors.RESET}`);
  }

  displayError(message: string): void {
    console.log(`${Colors.RED}Error: ${message}${Colors.RESET}`);
  }

  displayHint(move: string): void {
    console.log(`${Colors.YELLOW}Hint: Try ${move}${Colors.RESET}`);
  }
}