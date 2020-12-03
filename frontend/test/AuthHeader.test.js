import { authHeader } from "../src/service/AuthHeader";
require("jest-localstorage-mock");

test("Auth Header should generate header with user token", () => {
  localStorage.setItem("user_token", '"mock_token"');
  localStorage.setItem("user_id", '"mock_id"');

  const result1 = authHeader();
  expect(result1["Authorization"]).toBe("Bearer mock_token");
  expect(result1["Content-Type"]).toBe("application/json");

  localStorage.clear();
  const result2 = authHeader();
  expect(result2).toStrictEqual({});
});
