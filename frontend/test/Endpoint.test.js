import { backendPoint } from "../src/components/Endpoint";

test("endpoint test", () => {
  const result = backendPoint();
  expect(result).toBe("https://greloupis-backend.herokuapp.com");
});
