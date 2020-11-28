import * as func from "../src/util";

test("getSubstr should slice the first and last character of the string", () => {
  const result = func.getSubstr("'abc'");
  expect(result).toBe("abc");
});
