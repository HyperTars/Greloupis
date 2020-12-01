import { backendPoint } from "../src/components/Endpoint";

test("endpoint test", () => {
  const result = backendPoint();

  if (
    process.env.NODE_ENV === "test" ||
    process.env.NODE_ENV === "development"
  ) {
    // eslint-disable-next-line jest/no-conditional-expect
    expect(result).toBe("http://localhost:5000");
  } else {
    // eslint-disable-next-line jest/no-conditional-expect
    expect(result).toBe("https://greloupis-backend.herokuapp.com");
  }
});
