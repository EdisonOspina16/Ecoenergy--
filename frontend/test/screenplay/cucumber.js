const path = require("path");

const root = __dirname;
process.env.TS_NODE_PROJECT = path.join(root, "tsconfig.cucumber.json");

module.exports = {
  default: {
    paths: [path.join(root, "features", "**", "*.feature")],
    require: [
      path.join(root, "support", "**", "*.ts"),
      path.join(root, "steps", "**", "*.ts"),
    ],
    requireModule: ["ts-node/register"],
    format: ["progress", "summary"],
    timeout: 60000,
  },
};
