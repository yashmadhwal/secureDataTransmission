const GridConnections = artifacts.require("MappingAddressConnection");

module.exports = function (deployer) {
  deployer.deploy(GridConnections);
};
