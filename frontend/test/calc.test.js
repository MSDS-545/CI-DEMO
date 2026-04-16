import { add } from '../src/calc';

test('add works', () => {
  expect(add(2, 3)).toBe(5);
});