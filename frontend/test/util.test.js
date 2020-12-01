import * as func from "../src/util";
import moment from "moment";
require("jest-localstorage-mock");

let replaceMock = jest.fn();

delete window.location;
window.location = { replace: replaceMock };

afterEach(() => {
  replaceMock.mockClear();
});

test("convert timestamp to relative time", () => {
  const result = func.convertToRelativeTime("2020-01-01");
  expect(result).toBe(moment("2020-01-01").startOf("minutes").fromNow());
});

test("convert second to hour:minute:second format", () => {
  const result1 = func.secondTimeConvert(601);
  expect(result1).toBe("10:01");

  const result2 = func.secondTimeConvert(3661);
  expect(result2).toBe("01:01:01");
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

test("check local storage", () => {
  const result = func.isStorageEmpty();
  expect(result).toBe(true);
});

test("login check", () => {
  jest.spyOn(window, "alert").mockImplementation(() => {});

  func.loginCheck();
  expect(window.alert).toBeCalled();
  expect(window.location.replace).toBeCalled();
});

test("check avatar", () => {
  const result = func.generateAvatar();
  expect(result).toBe(
    "https://greloupis-images.s3.amazonaws.com/avatar-default-1.svg"
  );

  localStorage.setItem("user_thumbnail", "'abc'");
  const result2 = func.generateAvatar();
  expect(result2).toBe("abc");
});

test("check thumbnail", () => {
  const result = func.generateThumbnail("");
  expect(result).toBe(
    "https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png"
  );
});

test("generate uuid", () => {
  const result = func.uuid();
  expect(result.length).toBe(22);
});
