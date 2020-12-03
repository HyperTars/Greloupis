import logout from "../src/components/Logout";
require("jest-localstorage-mock");

test("Logout should clear localStorage", () => {
  logout();
  expect(localStorage.getItem("user_id")).toBe(null);
});
