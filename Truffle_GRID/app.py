import json
import random
import pandas as pd
from tqdm import tqdm


'''
These are two functions which will be used to establish/destablish connection between GRID,
based on this we will add/remove connection in GRID)connections e.g. A1-A2, A1-A3, etc.

And also it will be used to transact on the blockchain, which will record the connections and disconnections
'''

def establish_connection(from_,to_):

    #adding connections to GRID_connections set.
    try:
        GRID_connections.add(from_ +'-'+ to_)
        #Interacting with blockchain to transact (enableConnections).
        contract_MappingAddressConnection.functions.enableConnections(from_,to_).transact({'from':accounts_list[0]})
        return "Connection Establihed"
    except :
        return "Connection Already Exists"
        #later try except Exception as error to read from response

def destablish_connection(from_,to_):
    #removing connections from GRID_connections set.

    try:
        GRID_connections.remove(from_ +'-'+ to_)
        #Interacting with blockchain to transact.
        contract_MappingAddressConnection.functions.disableConnections(from_,to_).transact({'from':accounts_list[0]})
        return "Connection Destablished"
    except :
        return "No connection exists to disconnect"

def dataFrame_to_Dict(data):
    #data_dictionary = {}
    data_list = []
    for i,j in data.iteritems():
        dict_j = []
        for z in j:
            dict_j.append(str(z))
        #data_dictionary[str(i)] = dict_j
        data_list.append(dict_j)
    #return data_dictionary
    return data_list

def data_transaction(sender,receiver,iteration,amount):
        print(sender,receiver,iteration,amount)
        try:
            contract_passingArbitraryArguments.functions.passingValues(sender,receiver,iteration,amount).transact({'from':sender})
            return "OKo!"
        except:
            return "No connection"

#Establising Connections on blockchain
#Connection to Blockchain
from web3 import Web3
web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
# print("isConnected:",web3.isConnected())

#gettin lists of accounts available, Account[0] will be like an auditor account
accounts_list = web3.eth.accounts
# for i in accounts_list:
#     print(i)

#from index 1 to index 4, they will represent each GRID, so mapping them to regions A1, A2, A3, A4 resp.
GRID_accounts = {}
GRID_connections = set()

#Making Dictionary
for i in range(1,len(accounts_list)):
    GRID_accounts['A'+str(i)] = accounts_list[i]
# print(GRID_accounts)
# print()
#Printing then sequence wise
# for k, v in GRID_accounts.items():
#     print(k,':',v)

#First CONTRACT Deployment
with open('build/contracts/MappingAddressConnection.json') as f:
  first_migration = json.load(f)

first_migration_contract_address = first_migration['networks']['5777']['address']
first_migration_abi = first_migration['abi']
contract_MappingAddressConnection = web3.eth.contract(address=first_migration_contract_address, abi = first_migration_abi)

#Adding connections
establish_connection(GRID_accounts['A1'],GRID_accounts['A2'])
establish_connection(GRID_accounts['A1'],GRID_accounts['A3'])
establish_connection(GRID_accounts['A2'],GRID_accounts['A1'])
establish_connection(GRID_accounts['A2'],GRID_accounts['A4'])
establish_connection(GRID_accounts['A3'],GRID_accounts['A1'])
establish_connection(GRID_accounts['A3'],GRID_accounts['A4'])
establish_connection(GRID_accounts['A4'],GRID_accounts['A2'])
establish_connection(GRID_accounts['A4'],GRID_accounts['A3'])

A1_A2 = pd.read_csv('../Seperated_Excel_WD/A1_A2.csv', header=None)
A1_A3 = pd.read_csv('../Seperated_Excel_WD/A1_A3.csv', header=None)
A2_A1 = pd.read_csv('../Seperated_Excel_WD/A2_A1.csv', header=None)
A2_A4 = pd.read_csv('../Seperated_Excel_WD/A2_A4.csv', header=None)
A3_A1 = pd.read_csv('../Seperated_Excel_WD/A3_A1.csv', header=None)
A3_A4 = pd.read_csv('../Seperated_Excel_WD/A3_A4.csv', header=None)
A4_A2 = pd.read_csv('../Seperated_Excel_WD/A4_A2.csv', header=None)
A4_A3 = pd.read_csv('../Seperated_Excel_WD/A4_A3.csv', header=None)

#Importing CSV
#interating through data and putting in dictionary
data_A1_A2 = dataFrame_to_Dict(A1_A2)
data_A1_A3 = dataFrame_to_Dict(A1_A3)
data_A2_A1 = dataFrame_to_Dict(A2_A1)
data_A2_A4 = dataFrame_to_Dict(A2_A4)
data_A3_A1 = dataFrame_to_Dict(A3_A1)
data_A3_A4 = dataFrame_to_Dict(A3_A4)
data_A4_A2 = dataFrame_to_Dict(A4_A2)
data_A4_A3 = dataFrame_to_Dict(A4_A3)

#Data connection set:
GRID_Connections = {'A1_A2' : data_A1_A2,
                    'A1_A3' : data_A1_A3,
                    'A2_A1' : data_A2_A1,
                    'A2_A4' : data_A2_A4,
                    'A3_A1' : data_A3_A1,
                    'A3_A4' : data_A3_A4,
                    'A4_A2' : data_A4_A2,
                    'A4_A3' : data_A4_A3
                   }
#Second CONTRACT Deployment
with open('build/contracts/passingArbitraryArguments.json') as f:
  second_migration = json.load(f)

second_migration_contract_address = second_migration['networks']['5777']['address']
second_migration_abi = second_migration['abi']

contract_passingArbitraryArguments = web3.eth.contract(address=second_migration_contract_address, abi = second_migration_abi)

counter = 0
processing = True
while processing:
    for key in GRID_Connections.keys():
        try:
            sender, receiver = key.split("_")
            payload = GRID_Connections[key][counter]

            print(data_transaction(GRID_accounts[sender],GRID_accounts[receiver],counter,payload))

        except IndexError:
            processing = False
            break
    counter += 1

destablish_connection(GRID_accounts['A1'],GRID_accounts['A2'])
destablish_connection(GRID_accounts['A1'],GRID_accounts['A3'])
destablish_connection(GRID_accounts['A2'],GRID_accounts['A1'])
destablish_connection(GRID_accounts['A2'],GRID_accounts['A4'])
destablish_connection(GRID_accounts['A3'],GRID_accounts['A1'])
destablish_connection(GRID_accounts['A3'],GRID_accounts['A4'])
destablish_connection(GRID_accounts['A4'],GRID_accounts['A2'])
destablish_connection(GRID_accounts['A4'],GRID_accounts['A3'])
