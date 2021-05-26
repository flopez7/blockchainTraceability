// SPDX-License-Identifier: ECL-2.0
pragma solidity ^0.8.2;

contract Users{
    struct User 
    {
        string Name;
        string Surname;
        string Password;
    }
    
    mapping(string => User) public users;
    
    constructor(){
        
    }
    
    modifier isInList(string calldata _userId) 
    {
        require(length(users[_userId].Name) > 0, "Item not found");
        _;
    }
    
    function setUser(string calldata _userId, string calldata _name, string calldata _surname, string calldata _password) external
    {
        users[_userId].Name = _name;
        users[_userId].Surname = _surname;
        users[_userId].Password = _password;
    }
    
    function checkPassword(string calldata _userId, string calldata _password) external view isInList(_userId) returns (bool){
        return compareStrings(users[_userId].Password, _password);
    }
    
    // String manipulation functions
    function length(string memory str) internal pure returns (uint256) 
    {
        return bytes(str).length;
    }
    
    function compareStrings(string memory a, string memory b) internal pure returns (bool) {
        return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
    }
}