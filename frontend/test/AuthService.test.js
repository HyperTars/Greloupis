import AuthService from "../src/service/AuthService";
require("jest-localstorage-mock");

const OLD_ENV = process.env;

beforeEach(() => {
  jest.resetModules(); // most important - it clears the cache
  process.env = { ...OLD_ENV }; // make a copy
});

afterAll(() => {
  process.env = OLD_ENV; // restore old env
});

test("is auth", () => {
  const result = AuthService.isAuth();
  expect(result).toBe(false);
});

test("get current user test", () => {
  localStorage.setItem("user_token", '"mock_token"');
  const result = AuthService.getCurrentUser();
  expect(result).toBe("mock_token");
});

test("login", async () => {
  process.env.NODE_ENV = "production";

  await AuthService.login("hypertars", "hypertars");
  expect(localStorage.getItem("user_id")).toBe('"5f88f883e6ac4f89900ac983"');
  expect(localStorage.getItem("user_name")).toBe('"hypertars"');
});
