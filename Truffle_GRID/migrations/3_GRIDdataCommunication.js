var mydata = require("../build/contracts/MappingAddressConnection.json");
var address = mydata.networks['5777'].address;

const GridConnections = artifacts.require("passingArbitraryArguments");

module.exports = function (deployer) {
  deployer.deploy(GridConnections, address);
};
