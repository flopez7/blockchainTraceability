import json
from flask import Flask, Response, request, jsonify
from marshmallow import Schema, fields, ValidationError
from web3 import Web3
from web3.exceptions import ContractLogicError, BadFunctionCallOutput
from datetime import datetime
from flask_cors import CORS

BLOCKCHAIN_TYPE = "GANACHE"
#BLOCKCHAIN_TYPE = "INFURA"

# web3.py instance
if(BLOCKCHAIN_TYPE == 'GANACHE'):
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
    w3.eth.defaultAccount = w3.eth.accounts[1]
else:
    w3 = Web3(Web3.HTTPProvider("https://kovan.infura.io/v3/36d5f0ab413f4b4e9c6806a4f1dc2ded"))
    w3.eth.defaultAccount = '0xC1f8919336F2ac39009d10A92AF3447817B211c9'
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
    print(item)
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

# Get stored abi and contract_address
with open("./contract/data.json", 'r') as f:
    datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]

contract = w3.eth.contract(address=contract_address, abi=abi)

#For api validations
class ItemSchema(Schema):
    name = fields.String(required=True)
    place = fields.String(required=True)
    description = fields.String(required=True)

class UpdateItemNameSchema(Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)

class LocationSchema(Schema):
    id = fields.Int(required=True)
    place = fields.String(required=True)
    description = fields.String(required=True)

class UpdateLocationSchema(Schema):
    id = fields.Int(required=True)
    position = fields.Int(required=True)
    place = fields.String(required=True)
    description = fields.String(required=True)
    
class SourceSchema(Schema):
    id = fields.Int(required=True)
    source = fields.Int(required=True)
    
# Initializing flask app
app = Flask(__name__)
CORS(app)
# api to set new user every api call
@app.route("/blockchain/setItem", methods=['POST'])
def setItem():
    # Create the contract instance with the newly-deployed address
    
    body = request.get_json()
    try:
        result = ItemSchema().load(body)
    except ValidationError as err:
        return jsonify(**(err.valid_data),**(err.messages)), 422
     
    try:   
        id = contract.functions.next_id().call()

        if(BLOCKCHAIN_TYPE == 'GANACHE'):
            tx_hash = contract.functions.setItem(
                result['name'],result['place'],result['description']
            ).transact()
        else:
            nonce = w3.eth.get_transaction_count(w3.eth.defaultAccount)
            tx = contract.functions.setItem(
                result['name'],result['place'],result['description']
            ).buildTransaction({
                'nonce': nonce,
            })
            signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)
        item_data = contract.functions.getItem(id).call()
        return jsonify(parseItem(item_data,id)), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/setLocation", methods=['POST'])
def setLocation():
    # Create the contract instance with the newly-deployed address
    
    body = request.get_json()
    try:
        result = LocationSchema().load(body)
    except ValidationError as err:
        return jsonify(**(err.valid_data),**(err.messages)), 422

    try:
        if(BLOCKCHAIN_TYPE == 'GANACHE'):
            tx_hash = contract.functions.setLocation(
                result['id'],result['place'],result['description']
            ).transact()
        else:
            nonce = w3.eth.get_transaction_count(w3.eth.defaultAccount)
            tx = contract.functions.setLocation(
                result['id'],result['place'],result['description']
            ).buildTransaction({
                'nonce': nonce,
            })
            signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)
        item_data = contract.functions.getItem(result['id']).call()
        return jsonify(parseItem(item_data,result['id'])), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/setSource", methods=['POST'])
def setSource():
    # Create the contract instance with the newly-deployed address
    
    body = request.get_json()
    try:
        result = SourceSchema().load(body)
    except ValidationError as err:
        return jsonify(**(err.valid_data),**(err.messages)), 422

    try:
        if(BLOCKCHAIN_TYPE == 'GANACHE'):
            tx_hash = contract.functions.setSource(
                result['id'],result['source']
            ).transact()
        else:
            nonce = w3.eth.get_transaction_count(w3.eth.defaultAccount)
            tx = contract.functions.setSource(
                result['id'],result['source']
            ).buildTransaction({
                'nonce': nonce,
            })
            signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)
        item_data = contract.functions.getItem(result['id']).call()
        return jsonify(parseItem(item_data,result['id'])), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/updateItemName", methods=['PUT'])
def updateItemName():
    # Create the contract instance with the newly-deployed address
    
    body = request.get_json()
    try:
        result = UpdateItemNameSchema().load(body)
    except ValidationError as err:
        return jsonify(**(err.valid_data),**(err.messages)), 422

    try:
        if(BLOCKCHAIN_TYPE == 'GANACHE'):
            tx_hash = contract.functions.updateName(
                result['id'],result['name']
            ).transact()
        else:
            nonce = w3.eth.get_transaction_count(w3.eth.defaultAccount)
            tx = contract.functions.updateName(
                result['id'],result['name']
            ).buildTransaction({
                'nonce': nonce,
            })
            signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)
        item_data = contract.functions.getItem(result['id']).call()
        return jsonify(parseItem(item_data,result['id'])), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/updateLocation", methods=['PUT'])
def updateLocation():
    # Create the contract instance with the newly-deployed address
    
    body = request.get_json()
    try:
        result = UpdateLocationSchema().load(body)
    except ValidationError as err:
        return jsonify(**(err.valid_data),**(err.messages)), 422
       
    try:
        if(BLOCKCHAIN_TYPE == 'GANACHE'):
            tx_hash = contract.functions.updateLocation(
                result['id'],result['position'],result['place'],result['description']
            ).transact()
        else:
            nonce = w3.eth.get_transaction_count(w3.eth.defaultAccount)
            tx = contract.functions.updateLocation(
                result['id'],result['position'],result['place'],result['description']
            ).buildTransaction({
                'nonce': nonce,
            })
            signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)
        item_data = contract.functions.getItem(result['id']).call()
        return jsonify(parseItem(item_data,result['id'])), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/getItems", methods=['GET'])
def getItems():
    
    try:
        item_data = contract.functions.getAllItems().call()
        return jsonify(parseAllItems(item_data)), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': revert')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/getItem", methods=['GET'])
def getItem():
    id = int(request.args['id'])
    
    try:
        item_data = contract.functions.getItem(id).call()
        return jsonify(parseItem(item_data,id)), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/getLastLocation", methods=['GET'])
def getLastLocation():
    id = int(request.args['id'])
    
    try:
        item_data = contract.functions.getLastLocation(id).call()
        return jsonify(parseLocation(item_data)), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/getLocation", methods=['GET'])
def getLocation():
    id = int(request.args['id'])
    position = int(request.args['position'])
    
    try:
        item_data = contract.functions.getLocation(id,position).call()
        return jsonify(parseLocation(item_data)), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/getLocations", methods=['GET'])
def getLocations():
    id = int(request.args['id'])
    
    try:
        item_data = contract.functions.getAllLocations(id).call()
        return jsonify(parseAllLocations(item_data)), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/getSource", methods=['GET'])
def getSource():
    id = int(request.args['id'])
    
    try:
        item_data = contract.functions.getSource(id).call()
        return jsonify(parseSource(item_data)), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/getDerived", methods=['GET'])
def getDerived():
    id = int(request.args['id'])
    
    try:
        item_data = contract.functions.getDerived(id).call()
        return jsonify(parseAllItems(item_data)), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/deleteItem", methods=['DELETE'])
def deleteItem():
    id = int(request.args['id'])

    try:
        if(BLOCKCHAIN_TYPE == 'GANACHE'):
            tx_hash = contract.functions.removeItem(id).transact()
        else:
            nonce = w3.eth.get_transaction_count(w3.eth.defaultAccount)
            tx = contract.functions.removeItem(id).buildTransaction({
                'nonce': nonce,
            })
            signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)
        item_data = contract.functions.getAllItems().call()
        return jsonify(parseAllItems(item_data)), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/deleteLastLocation", methods=['DELETE'])
def deleteLastLocation():
    id = int(request.args['id'])

    try:
        if(BLOCKCHAIN_TYPE == 'GANACHE'):
            tx_hash = contract.functions.removeLastLocation(id).transact()
        else:
            nonce = w3.eth.get_transaction_count(w3.eth.defaultAccount)
            tx = contract.functions.removeLastLocation(id).buildTransaction({
                'nonce': nonce,
            })
            signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)
        item_data = contract.functions.getItem(id).call()
        return jsonify(parseItem(item_data,id)), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422
    

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)