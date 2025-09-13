import { Colors, Levels, Styles } from '../utils/core';

describe('Core utilities', () => {
  describe('Colors', () => {
    it('should have defined color constants', () => {
      expect(Colors.RESET).toBeDefined();
      expect(Colors.RED).toBeDefined();
      expect(Colors.GREEN).toBeDefined();
      expect(Colors.BOLD).toBeDefined();
    });

    it('should have background colors', () => {
      expect(Colors.Backgrounds.LIGHT).toBeDefined();
      expect(Colors.Backgrounds.DARK).toBeDefined();
    });
  });

  describe('Styles', () => {
    it('should have padding constants', () => {
      expect(Styles.PADDING_SMALL).toBe('  ');
      expect(Styles.PADDING_MEDIUM).toBe('      ');
      expect(Styles.PADDING_LARGE).toBe('          ');
    });
  });

  describe('Levels', () => {
    it('should have level constants', () => {
      expect(Levels.ONE).toBe(1);
      expect(Levels.EIGHT).toBe(8);
    });

    it('should normalize level values correctly', () => {
      expect(Levels.levelOfInt(0)).toBe(1);
      expect(Levels.levelOfInt(5)).toBe(5);
      expect(Levels.levelOfInt(10)).toBe(8);
    });

    it('should return correct skill values', () => {
      expect(Levels.value(1)).toBe(1);
      expect(Levels.value(8)).toBe(20);
    });
  });
});