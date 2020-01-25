pragma solidity ^0.5.0;


contract BetCoins {
    address payable owner = msg.sender;
    string symbol = "BetCoins";

    mapping(address => uint) balances;

    function balance() public view returns(uint) {
        return balances[msg.sender];
    }

    function Win(address recipient, uint value) public {
        value = (value*3)/2;
        balances[msg.sender] -= value;
        balances[recipient] += value;
    }
    function PlaceBet(address bettor, uint value) public {
        balances[bettor] -= value;
        balances[msg.sender] += value;
    }
    
    function AccountInitialization(address recipient, uint value) public {
        value = 100;
        balances[msg.sender] -= value;
        balances[recipient] += value;
    }
    function mint(address recipient, uint value) public {
        require(msg.sender == owner, "You do not have permission to mint tokens!");
        balances[recipient] += value;
    }
}
