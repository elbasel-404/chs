export class Colors {
  static readonly RESET = '\x1b[49;0m';
  static readonly DARK = '\x1b[38;5;232;1m';
  static readonly LIGHT = '\x1b[38;5;231;1m';
  static readonly WHITE = '\x1b[38;5;231;0m';
  static readonly GREEN = '\x1b[38;5;2;1m';
  static readonly YELLOW = '\x1b[38;5;226;1m';
  static readonly ORANGE = '\x1b[38;5;208;1m';
  static readonly RED = '\x1b[38;5;1m';
  static readonly GRAY = '\x1b[38;5;242m';
  static readonly BOLD = '\x1b[1m';
  static readonly UNDERLINE = '\x1b[4m';
  static readonly DULL_GRAY = '\x1b[38;5;238;1m';
  static readonly DULL_GREEN = '\x1b[38;5;28;1m';

  static readonly Backgrounds = {
    GREEN_DARK: '\x1b[48;5;136;1m',
    GREEN_LIGHT: '\x1b[48;5;143;1m',
    PURPLE_DARK: '\x1b[48;5;176;1m',
    PURPLE_LIGHT: '\x1b[48;5;177;1m',
    DARK: '\x1b[48;5;172;1m',
    LIGHT: '\x1b[48;5;215;1m',
    BLACK: '\x1b[48;5;232;1m',
    WHITE: '\x1b[48;5;15;1m',
    RED: '\x1b[48;5;9;1m'
  };
}

export class Styles {
  static readonly PADDING_SMALL = '  ';
  static readonly PADDING_MEDIUM = '      ';
  static readonly PADDING_LARGE = '          ';
}

export class Levels {
  static readonly ONE = 1;
  static readonly TWO = 2;
  static readonly THREE = 3;
  static readonly FOUR = 4;
  static readonly FIVE = 5;
  static readonly SIX = 6;
  static readonly SEVEN = 7;
  static readonly EIGHT = 8;

  static levelOfInt(n: number): number {
    return Math.max(1, Math.min(n, 8));
  }

  static value(level: number): number {
    const levels = [1, 4, 7, 10, 12, 14, 17, 20];
    return levels[level - 1];
  }
}