global.console = {
  ...console,
  log: jest.fn(),
  warn: jest.fn(),
};

global.fetch = require("node-fetch");
