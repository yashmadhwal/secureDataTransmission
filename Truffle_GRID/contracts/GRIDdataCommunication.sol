pragma solidity <0.6.5;
pragma experimental ABIEncoderV2;

import './GridConnections.sol';



contract passingArbitraryArguments {

    MappingAddressConnection maps;

    event NewTrade(
        address indexed _from,
        address indexed to,
        uint indexed iteration,
        string[] amount
        );

    constructor(address addr) public {
        maps = MappingAddressConnection(addr);
    }

    function passingValues(address _sender, address _to, uint _iteration, string[] memory _value) public {
        require(maps.connections(_sender,_to),"Connection Not Established");
          emit NewTrade(_sender, _to, _iteration, _value);
    }

    function checkingstate(address _sender, address _to) view public returns(bool){
       return maps.connections(_sender,_to);
    }

}
