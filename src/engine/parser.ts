export class FenParser {
  private fen: string;

  constructor(fen: string) {
    this.fen = fen;
  }

  updateFen(fen: string): void {
    this.fen = fen;
  }

  getFen(): string {
    return this.fen;
  }

  // Parse FEN to get board position
  getBoardPosition(): string[][] {
    const fenParts = this.fen.split(' ');
    const position = fenParts[0];
    const rows = position.split('/');
    
    const board: string[][] = [];
    
    for (const row of rows) {
      const boardRow: string[] = [];
      
      for (const char of row) {
        if (char >= '1' && char <= '8') {
          // Empty squares
          const emptyCount = parseInt(char, 10);
          for (let i = 0; i < emptyCount; i++) {
            boardRow.push('');
          }
        } else {
          // Piece
          boardRow.push(char);
        }
      }
      
      board.push(boardRow);
    }
    
    return board;
  }

  getActiveColor(): 'w' | 'b' {
    const fenParts = this.fen.split(' ');
    return fenParts[1] as 'w' | 'b';
  }

  getCastlingRights(): string {
    const fenParts = this.fen.split(' ');
    return fenParts[2] || '-';
  }

  getEnPassantTarget(): string {
    const fenParts = this.fen.split(' ');
    return fenParts[3] || '-';
  }

  getHalfmoveClock(): number {
    const fenParts = this.fen.split(' ');
    return parseInt(fenParts[4] || '0', 10);
  }

  getFullmoveNumber(): number {
    const fenParts = this.fen.split(' ');
    return parseInt(fenParts[5] || '1', 10);
  }
}