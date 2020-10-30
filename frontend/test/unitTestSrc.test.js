import sumAB from '../src/unitTestSrc';

test('sum(2 + 2) equals 4', () => {
    const result = sumAB(2, 2);
    expect(result).toBe(4);
})
