// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FakeProductDetection {
    address public owner;
    
    uint product_id = 0;
    
    struct Manufacturer {
        bool exists;
		string name;
		address _address;
	}
    
    struct Product {
        bool exists;
        uint productId;
        uint256 crawl_timestramp;
        string productName;
        uint retail_price;
        uint discounted_price;
        string brand;
        bool isAuthentic;
        address manufacturer;
    }
    
    mapping(address => Manufacturer) public manufacturers;
    mapping(uint => Product) public products;
    uint public productCount;
    
    event ManufacturerCreated(string name, address _address);
    event ProductAdded(uint product_id, uint256 crawl_timestramp, string product_Name, string pid, uint retail_price, uint discounted_price, string brand, bool is_authentic, address manufacturer);
    event OwnershipUpdated(uint id, address newOwner);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }
    
    function createManufacturer(string memory _name, address _address) public {
		require(msg.sender == owner, "Only owner is authorised to create a manufacturer!");

		Manufacturer storage m = manufacturers[_address];
		m.exists = true;
		m.name = _name;
		m._address = _address;
		emit ManufacturerCreated(_name, _address);
	}

	function createProduct(string memory _name, string memory _model) public {
		require(manufacturers[msg.sender].exists == true, "You are not a Manufacturer!");

		Product storage p = products[_id];
		p.exists = true;
		p.productId = product_id;
		p.product_name = _name;
		p.brand = _brand;
		p.manufacturer = msg.sender;
		
		p.owners.push(msg.sender);
        
        product_id++;
		emit ProductCreated(product_id-1, msg.sender);
	}

	function getProduct(uint _id) public view returns(Product memory) {
		return products[_id];
	}

    
    function verifyProduct(uint uniqueId) public view returns (bool) {
        return products[_id].isAuthentic;
    }
}
    
