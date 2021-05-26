from datetime import datetime
from solcx import compile_source
import json

BLOCKCHAIN_TYPE = "GANACHE"
#BLOCKCHAIN_TYPE = "INFURA"

private_key = 'a2353cf143ee9af9686aba2dcef35ce765014bbaced70d4947dce7acdca3b5db'

def parseItem (item, id): 
    parsed = {}
    parsed['id'] = id
    parsed['name'] = item[0]
    parsed['locations'] = []
    for i in range(len(item[1])):
        location = {}
        location['place'] = item[1][i][0]
        location['description'] = item[1][i][1]
        location['datetime'] = datetime.fromtimestamp(item[1][i][2]).strftime("%m/%d/%Y, %H:%M:%S")
        parsed['locations'].append(location)
    parsed['source'] = item[2]
    return parsed

def parseLocation(location):
    parsed = {}
    parsed['place'] = location[0]
    parsed['description'] = location[1]
    parsed['datetime'] = datetime.fromtimestamp(location[2]).strftime("%m/%d/%Y, %H:%M:%S")
    return parsed

def parseSource (item):
    parsed = {}
    parsed['id'] = item[0]
    parsed['name'] = item[1][0]
    parsed['locations'] = []
    for i in range(len(item[1][1])):
        location = {}
        location['place'] = item[1][1][i][0]
        location['description'] = item[1][1][i][1]
        location['datetime'] = datetime.fromtimestamp(item[1][1][i][2]).strftime("%m/%d/%Y, %H:%M:%S")
        parsed['locations'].append(location)
    parsed['source'] = item[1][2]
    return parsed

def parseAllItems(items):
    parsed = []
    for i in range(len(items[0])):
        item = {}
        item['id'] = items[0][i]
        item['name'] = items[1][i][0]
        item['locations'] = []
        for j in range(len(items[1][i][1])):
            location = {}
            location['place'] = items[1][i][1][j][0]
            location['description'] = items[1][i][1][j][1]
            location['datetime'] = datetime.fromtimestamp(items[1][i][1][j][2]).strftime("%m/%d/%Y, %H:%M:%S")
            item['locations'].append(location)
        item['source'] = items[1][i][2]
        parsed.append(item)
    return parsed

def parseAllLocations(items):
    print(items[0])
    parsed = {}
    parsed['locations'] = []
    for i in range(len(items)):
        location = {}
        location['place'] = items[i][0]
        location['description'] = items[i][1]
        location['datetime'] = datetime.fromtimestamp(items[i][2]).strftime("%m/%d/%Y, %H:%M:%S")
        parsed['locations'].append(location)
    return parsed

#Compilar el smart contract
def compileSourceFile(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    return compile_source(source)

#Despliegue del contrato
def deploy_contract(w3, contract_interface):
    if(BLOCKCHAIN_TYPE == 'GANACHE'):
        tx_hash = w3.eth.contract(
            abi=contract_interface['abi'],
            bytecode=contract_interface['bin']).constructor().transact()
    else:
        nonce = w3.eth.get_transaction_count(w3.eth.defaultAccount)
        tx = w3.eth.contract(
            abi=contract_interface['abi'],
            bytecode=contract_interface['bin']).constructor().buildTransaction({
            'nonce': nonce,
            })
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
   
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    return tx_receipt.contractAddress

def get_contracts(w3):
    compiled_sol = compileSourceFile('./contract/Traceability.sol')
    contract_id_traceability, contract_interface_traceability = compiled_sol.popitem()
    compiled_sol = compileSourceFile('./contract/Users.sol')
    contract_id_users, contract_interface_users = compiled_sol.popitem()

    try:
        # Get stored abi and contract_address
        with open("./contract/data.json", 'r') as f:
            datastore = json.load(f)
            traceability = w3.eth.contract(
                address=datastore[BLOCKCHAIN_TYPE]['traceability']['address'], 
                abi=contract_interface_traceability['abi']
                )
            users = w3.eth.contract(
                address=datastore[BLOCKCHAIN_TYPE]['users']['address'], 
                abi=contract_interface_users['abi']
                )

    except:
        address = deploy_contract(w3, contract_interface_traceability)
        abi = contract_interface_traceability['abi']

        traceability = w3.eth.contract(address=address, abi=abi)

        data = {}
        data[BLOCKCHAIN_TYPE] = {}
        data[BLOCKCHAIN_TYPE]['traceability'] = {}
        data[BLOCKCHAIN_TYPE]['traceability'] = {}
        data[BLOCKCHAIN_TYPE]['traceability']['address'] = address

        address = deploy_contract(w3, contract_interface_users)
        abi = contract_interface_users['abi']

        users = w3.eth.contract(address=address, abi=abi)

        data[BLOCKCHAIN_TYPE]['users'] = {}
        data[BLOCKCHAIN_TYPE]['users']['address'] = address

        with open("./contract/data.json", 'w') as f:
            json.dump(data, f)

    return traceability, users