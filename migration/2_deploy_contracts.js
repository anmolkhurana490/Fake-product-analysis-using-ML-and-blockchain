const MyApp = artifacts.require("/FakeProductDetection.sol");

module.exports = function(deployer) {
	deployer.deploy(FakeProductDetection);
};