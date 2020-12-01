import * as func from "../src/components/FetchData";
require("jest-localstorage-mock");

const TEST_NAME = "hypertars";
const TEST_ID = "5f88f883e6ac4f89900ac983";

const OLD_ENV = process.env;

beforeEach(() => {
  jest.resetModules(); // most important - it clears the cache
  process.env = { ...OLD_ENV }; // make a copy
});

afterAll(() => {
  process.env = OLD_ENV; // restore old env
});

test("user endpoints", async () => {
  process.env.NODE_ENV = "production";

  // user login
  const loginResult = await func.userLogin({
    user: TEST_NAME, // support both name and email
    user_password: TEST_NAME,
  });
  expect(loginResult.user_id).toBe(TEST_ID);
  expect(loginResult.user_name).toBe(TEST_NAME);

  // user get info
  const getUserResult = await func.getUserInfo(TEST_ID);
  expect(getUserResult.body.user.user_id).toBe(TEST_ID);
  expect(getUserResult.body.user.user_name).toBe(TEST_NAME);
});

test("video endpoints", async () => {
  process.env.NODE_ENV = "production";

  // getVideoInfo
  const getVideoResult = await func.getVideoInfo("5fc3fc847c5e2989dac5dbd4");
  expect(getVideoResult.body.video_id).toBe("5fc3fc847c5e2989dac5dbd4");
  expect(getVideoResult.body.video_title).toBe("Shanghai in the mist");
});

test("search endpoints", async () => {
  process.env.NODE_ENV = "production";

  // search user
  const searchUserResult = await func.searchUser("hypertars");
  expect(searchUserResult["body"][0]["user_name"]).toBe("hypertars");
  expect(searchUserResult["body"][0]["user_email"]).toBe("hypertars@gmail.com");

  // search video
  const searchVideoResult = await func.searchVideo("shanghai");
  expect(searchVideoResult["body"][0]["video_title"]).toBe(
    "Shanghai in the mist"
  );

  // search top video
  const searchTopResult = await func.searchTopVideo("video_view");
  expect(searchTopResult["body"][0]["video_title"]).toBe(
    "Shanghai in the mist"
  );
});
