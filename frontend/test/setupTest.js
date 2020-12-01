global.console = {
  ...console,
  warn: jest.fn(),
};

global.fetch = require("node-fetch");
