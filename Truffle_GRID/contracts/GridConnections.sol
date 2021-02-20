// SPDX-License-Identifier: MIT
pragma solidity <0.6.4;

contract MappingAddressConnection {

    address _owner;

    //establishing Owner of smartContract
    constructor() public{
        _owner = msg.sender;
    }

    event gridconnectionEvent(
        address _from,
        address _to,
        bool _status);

    mapping(address => mapping(address => bool)) public connections;

    //establishing connections:
    function enableConnections(address _from, address _to) public onlyOwner NotSelf(_from,  _to){
        // checking that connection not already true
        require(connections[_from][_to] == false, 'connections already established');
        connections[_from][_to] = true;

        emit gridconnectionEvent(_from, _to, true);
    }

    //Disableling connections:
    function disableConnections(address _from, address _to) public NotSelf(_from,  _to){
        // checking that connection not already false
        require(connections[_from][_to] == true, 'connections not established');
        connections[_from][_to] = false;

        emit gridconnectionEvent(_from, _to, true);
    }

    modifier onlyOwner{
        require(msg.sender == _owner,"You can't Deploy, SORRY!!!!");
        _;
    }

    modifier NotSelf(address _from, address _to) {
        require(_from != _to, "Can't Establish connections with self");
        _;
    }
}
