import * as func from "../src/util";
import moment from "moment";

test("convert timestamp to relative time", () => {
  const result = func.convertToRelativeTime("2020-01-01");
  expect(result).toBe(moment("2020-01-01").startOf("minutes").fromNow());
});

test("convert second to hour:minute:second format", () => {
  const result = func.secondTimeConvert(3661);
  expect(result).toBe("01:01:01");
});

test("convert timestamp to yy:mm:dd", () => {
  const result = func.dateConvert("2020-01-01 12:00:00");
  expect(result).toBe("2020-01-01");
});

test("getSubstr should slice the first and last character of the string", () => {
  const result = func.getSubstr("'abc'");
  expect(result).toBe("abc");
});

test("set the max display length of given string", () => {
  const result = func.ellipsifyStr("abcdefghijkl", 5);
  expect(result).toBe("abcde...");
});

test("generate uuid", () => {
  const result = func.uuid();
  expect(result.length).toBe(22);
});
