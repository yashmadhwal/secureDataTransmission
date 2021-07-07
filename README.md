# Application of blockchain for secure data transmission in distributed state estimation
### Blockchain based decentralized applicaton for secure data transmission between GRID areas.

This is repository for running a Decentralized Application (DAPP), for GRID communication

### Features:

- Deploy blockchain application on local computer
- Easy to run python scripts
- Experiment results based on arbitrary input on the proposed model

### Prerequisites
- Download and install [Python 3.7](https://www.python.org/downloads/)
- Instal [Node.js](https://nodejs.org/en/download/) and npm (comes with node)
- [Git](https://git-scm.com/downloads)
- Download and install [Ganache UI](https://www.trufflesuite.com/ganache).

### Installation
After download and installing the above prerequisites, Now, it will be time for installing required libraries. There might be chances that some of the required modules comes preinstalled.

Open terminal or command prompt of you computer and run the following commands:
| Libraries | Command |
| ------ | ------ |
| [Web3Py](https://web3py.readthedocs.io/en/stable/quickstart.html#installation) | `pip install web3` |
| [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html) | `pip install pandas` |
| [Numpy](https://numpy.org/install/) | `pip install numpy` |
| [Matplot](https://matplotlib.org/stable/users/installing.html) | `pip install matplotlib` |

**Note**: Although, the above mentioned scripts should be sufficient to run the application. If any problem arises, please check the python version and library that you are running.

### Cloning the repository
Download or clone the repository. Open terminal or command prompt and redirect to folder Truffle_GRID
`cd Truffle_GRID`

### Running DApp

Once in the folder **Truffle_GRID**.
Open Ganache UI, It will present you with the set of Ethereum Wallets with 100ETH each. For this prototype we require minimum of 5 wallets, so if the number of wallets are less than 5, please configue the number of accounts in Ganache's settings, such that the number of wallets are 5 or more. If the accounts are more, it is normal, but we will require only 5.

**Note**: If you want same Wallets as the following example, copy-paste the Mnemonic in the settings
*`magnet fatal pill denial such kidney pear learn fever lab mom weird`*

GRID's Wallets:
| Wallet | Owner |
| ------ | ------ |
| `0x9CC190A96e287418e5DeBec96Ea139ca5db7c9e8` | *Auditor*|
| `0xda8F98eD2b9dC061a876C6039Fe58E8272af0AF7` | *Area_1* |
| `0x2Fd6Bed5ca468f1f3C78adaD7BdcE8f97f8Fd547` | *Area_2* |
| `0xC0818f17A1178b2Da1E2E6937aeE6A8E6Ee8D07e` | *Area_3* |
| `0xb6d35CD088a35BE0A8d18f7d6b1e1781430DD045` | *Area_4* |

In the terminal, first compile the smart contract:
`truffle compile`
And now, migrate it to the blockchain:
`truffle migrate`

On ganache UI (under **Transactions** tab), you will see three contracts (**CONTRACT CREATION**) that were deployed from the Auditor's wallet:
- Migration Contract
- GridConnections
- GRIDdataCommunication

Following this, run the python file:
`python app.py`

You will see, the transaction and data transfer along with payload between different wallets (GRID Areas). Tis python scripts contains 3 parts:
- Establishing Connections: The transaction in a smart contract can happen only if there is connection established between GRIDS. The smart contract [GRID Connections](https://github.com/yashmadhwal/secureDataTransmission/blob/main/Truffle_GRID/contracts/GridConnections.sol) is deployed only by the auditor and upon the request can establish or remove connection.
- Data communications: Smart contract [Data Commuications](https://github.com/yashmadhwal/secureDataTransmission/blob/main/Truffle_GRID/contracts/GRIDdataCommunication.sol) is deployed by Auditor, but the communication happens directly among the GRID areas.
- Removing Connection: Method is in the contract [GRID Connections](https://github.com/yashmadhwal/secureDataTransmission/blob/main/Truffle_GRID/contracts/GridConnections.sol), where only the auditor can remove the connections.

You can explore Ganache UI to explore blockchain or use web3py library for python to get detailed analysis.

Based on this contract, we conducted the experiments.

## Smart contracts
The repository contains 3 smart contracts:
- [Migration](https://github.com/yashmadhwal/secureDataTransmission/blob/main/Truffle_GRID/contracts/Migrations.sol)
    The Migrations contract keeps track of which migrations were done on the blockchain network. Once a contract(s) are ready for deployment on the network, we do it by command `truffle migrate`.

- [GridConnections](https://github.com/yashmadhwal/secureDataTransmission/blob/main/Truffle_GRID/contracts/GridConnections.sol)
GridConnection smart contract is deployed by Auditor and is responsible for establishment and disbandment of connection among the GRIDS. The smart contract has modifier `onlyOwner` that makes sure the transaction to establish and disbandment can only be transacted by owner of the smart contract, i.e., the auditor.
With every function call of `enableConnections(_from, _to)` and `disableConnections(_from, _to) `, event is triggered from the blockchain that emits message `connection: _from,_to, true/false`.

- [GRIDdataCommunication](https://github.com/yashmadhwal/secureDataTransmission/blob/main/Truffle_GRID/contracts/GRIDdataCommunication.sol)
Based on the Connections that are established by Auditor in the smart contract [GridConnections](https://github.com/yashmadhwal/secureDataTransmission/blob/main/Truffle_GRID/contracts/GridConnections.sol). The auditor deploys additional contract `GRIDdataCommunication`, which communicates with `GRIDconnections` and is updated with new connections/disconnection among GRIDs.
Bases on the connection status, for example, connection status true between the sender of the data (lets say *Area_1*) to receiver of the data (*Area_2*), only the Sender can send the data by executing the function `passingValues(_sender,_to,_iteration,_value)`.  

    | parameter | Type | Description |
    | ------ | ------ |------ |
    | **_sender** | *address*|Transaction executor and sender of data (GRID computation values)|
    | **_to** | *address* |Recipient (GRID computation values)|
    | **_iteration** | *uint* | Incrementing round of data transfer |
    | **_value** | *array* | Payload of data that is transfered, with each iteration different datas of different size transfered|
