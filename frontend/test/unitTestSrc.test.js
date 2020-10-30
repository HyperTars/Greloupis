import functions  from '../src/unitTestSrc';

test('sum(2 + 2) equals 4', () => {
    expect(functions.sum(2, 2)).toBe(4);
})
