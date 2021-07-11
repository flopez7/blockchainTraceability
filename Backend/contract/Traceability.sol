// SPDX-License-Identifier: ECL-2.0
pragma solidity ^0.8.2;

contract Traceability 
{
    struct Location 
    {
        string place;
        string description;
        uint256 timestamp;
    }

    struct Item 
    {
        string name;
        Location[] locations;
        uint256 source;
    }

    uint256 public next_id;

    mapping(uint256 => Item) public items;

    constructor() 
    {
        next_id = 1;
    }

    modifier isInList(uint256 _id) 
    {
        require(length(items[_id].name) > 0, "Item not found");
        _;
    }
    
    modifier notEmptyList 
    {
        require(getNumItems() > 0, "No items");
        _;
    }

    function setItem(string calldata _name, string calldata _place, string calldata _description) external
    {
        items[next_id].name = _name;
        items[next_id].locations.push(Location(_place, _description, block.timestamp));
        next_id++;
    }
    
    function setSource(uint256 _id, uint256 _source) external isInList(_id) isInList(_source)
    {
        items[_id].source = _source;
    }

    function setLocation(uint256 _id, string calldata _place, string calldata _description) external isInList(_id)
    {
        items[_id].locations.push(Location(_place, _description, block.timestamp));
    }

    function getAllLocations(uint256 _id) external view isInList(_id) returns(Location[] memory)
    {
        return(items[_id].locations);
    }
    
    function getAllItems() view external notEmptyList returns(uint256[] memory, Item[] memory)
    {
        uint256 numItems = getNumItems();
        Item[] memory allItems = new Item[](numItems);
        uint256[] memory allIds = new uint256[](numItems);
        uint256 current = 0;
        for(uint256 i=1; i < next_id; i++){
            if(length(items[i].name) > 0){
                allItems[current] = items[i];
                allIds[current] = i;
                current++;
            }
        }
        return (allIds, allItems);
    }
    
    function getItem(uint256 _id) external view isInList(_id) returns (Item memory)
    {
        
        return (items[_id]);
    }

    function getLocation(uint256 _id, uint256 _position) external view isInList(_id) returns (Location memory)
    {
        return (items[_id].locations[_position]);
    }

    function getLastLocation(uint256 _id) external view isInList(_id) returns (Location memory)
    {
        return (items[_id].locations[items[_id].locations.length - 1]);
    }
    
    function getSource(uint256 _id) external view isInList(_id) returns (uint256, Item memory)
    {
        require(items[_id].source>0, "Item has no source");
        return (items[_id].source, items[items[_id].source]);
    }
    
    function getDerived(uint256 _id) external view isInList(_id) returns (uint256[] memory, Item[] memory)
    {
        uint256 numItems = 0;
        for(uint256 i=1; i < next_id; i++){
            if(length(items[i].name) > 0 && items[i].source != 0 && i != _id && items[i].source == _id){
                numItems++;
            }
        }
        require(numItems>0, "Item has no derivates");
        Item[] memory derived = new Item[](numItems);
        uint256[] memory itemsIds = new uint256[](numItems);
        uint256 current = 0;
        for(uint256 i=1; i < next_id; i++){
            if(length(items[i].name) > 0 && items[i].source != 0 && i != _id && items[i].source == _id){
                derived[current] = items[i];
                itemsIds[current] = i;
                current++;
            }
        }
        return (itemsIds, derived);
    }
    
    function getNumItems() public view returns (uint256)
    {
        uint256 numItems = 0;
        for(uint256 i=1; i < next_id; i++){
            if(length(items[i].name) > 0){
                numItems++;
            }
        }
        return numItems;
    }

    function removeItem(uint256 _id) external isInList(_id) 
    {
        delete items[_id];
    }
    
    function removeLastLocation(uint256 _id) external isInList(_id) 
    {
        items[_id].locations.pop();
    }
    
    function updateName(uint256 _id, string calldata _name) external isInList(_id)
    {
        items[_id].name = _name;
    }

    function updateLocation(uint256 _id, uint256 _position, string calldata _place, string calldata _description) external isInList(_id)
    {
        require(items[_id].locations.length>0, "No locations");
        items[_id].locations[_position].place = _place;
        items[_id].locations[_position].description = _description;
    }

    // String manipulation functions
    function length(string memory str) internal pure returns (uint256) 
    {
        return bytes(str).length;
    }
}