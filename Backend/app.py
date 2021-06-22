from flask import Flask, Response, request, jsonify
from marshmallow import ValidationError
from marshmallow.fields import String
from web3 import Web3
from web3.exceptions import ContractLogicError, BadFunctionCallOutput
from flask_cors import CORS
import functions
import validators

#BLOCKCHAIN_TYPE = "GANACHE"
BLOCKCHAIN_TYPE = "INFURA"

# web3.py instance
if(BLOCKCHAIN_TYPE == 'GANACHE'):
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
    w3.eth.defaultAccount = w3.eth.accounts[1]
else:
    w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/36d5f0ab413f4b4e9c6806a4f1dc2ded"))
    w3.eth.defaultAccount = '0xC1f8919336F2ac39009d10A92AF3447817B211c9'
    private_key = 'a2353cf143ee9af9686aba2dcef35ce765014bbaced70d4947dce7acdca3b5db'

contract, users = functions.get_contracts(w3)

# Initializing flask app
app = Flask(__name__)
CORS(app)
# api to set new user every api call
@app.route("/blockchain/setItem", methods=['POST'])
def setItem():
    # Create the contract instance with the newly-deployed address
    
    body = request.get_json()
    try:
        result = validators.ItemSchema().load(body)
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
        return jsonify(functions.parseItem(item_data,id)), 200
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
        result = validators.LocationSchema().load(body)
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
        return jsonify(functions.parseItem(item_data,result['id'])), 200
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
        result = validators.SourceSchema().load(body)
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
        return jsonify(functions.parseItem(item_data,result['id'])), 200
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
        result = validators.UpdateItemNameSchema().load(body)
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
        return jsonify(functions.parseItem(item_data,result['id'])), 200
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
        result = validators.UpdateLocationSchema().load(body)
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
        return jsonify(functions.parseItem(item_data,result['id'])), 200
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
        return jsonify(functions.parseAllItems(item_data)), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/blockchain/getItem", methods=['GET'])
def getItem():
    id = int(request.args['id'])
    
    try:
        item_data = contract.functions.getItem(id).call()
        return jsonify(functions.parseItem(item_data,id)), 200
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
        return jsonify(functions.parseLocation(item_data)), 200
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
        return jsonify(functions.parseLocation(item_data)), 200
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
        return jsonify(functions.parseAllLocations(item_data)), 200
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
        return jsonify(functions.parseSource(item_data)), 200
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
        return jsonify(functions.parseAllItems(item_data)), 200
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
        return jsonify(functions.parseAllItems(item_data)), 200
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
        return jsonify(functions.parseItem(item_data,id)), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422
    

@app.route("/user/setUser", methods=['POST'])
def setUser():
    body = request.get_json()
    try:
        result = validators.UserSchema().load(body)
    except ValidationError as err:
        return jsonify(**(err.valid_data),**(err.messages)), 422

    try:
        if(BLOCKCHAIN_TYPE == 'GANACHE'):
            tx_hash = users.functions.setUser(
                result['id'],result['name'],result['surname'],result['email'],result['password']
            ).transact()
        else:
            nonce = w3.eth.get_transaction_count(w3.eth.defaultAccount)
            tx = users.functions.setUser(
                result['id'],result['name'],result['surname'],result['email'],result['password']
            ).buildTransaction({
                'nonce': nonce,
            })
            signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)
        return jsonify({"result": "Succesfull"}), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422
        
@app.route("/user/checkPassword", methods=['POST'])
def checkPassword():
    body = request.get_json()
    try:
        result = validators.PasswordSchema().load(body)
    except ValidationError as err:
        return jsonify(**(err.valid_data),**(err.messages)), 422
    
    try:
        if(users.functions.checkPassword(result['id'],result['password']).call()):
            return jsonify({"result": "true"}), 200
        else:
            return jsonify({"result": "false"}), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/user/updateUser", methods=['PUT'])
def updateUser():
    body = request.get_json()
    try:
        result = validators.UserSchema().load(body)
    except ValidationError as err:
        return jsonify(**(err.valid_data),**(err.messages)), 422

    try:
        if(BLOCKCHAIN_TYPE == 'GANACHE'):
            tx_hash = users.functions.updateUser(
                result['id'],result['name'],result['surname'],result['email'],result['password']
            ).transact()
        else:
            nonce = w3.eth.get_transaction_count(w3.eth.defaultAccount)
            tx = users.functions.updateUser(
                result['id'],result['name'],result['surname'],result['email'],result['password']
            ).buildTransaction({
                'nonce': nonce,
            })
            signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)
        return jsonify({"result": "Succesfull"}), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422


@app.route("/user/getUser", methods=['GET'])
def getUser():
    id = request.args['id']
    print(id)
    try:
        user_data = users.functions.users(id).call()
        return jsonify(functions.parseUser(user_data,id)), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

@app.route("/user/deleteUser", methods=['DELETE'])
def deleteUser():
    id = request.args['id']
    try:
        if(BLOCKCHAIN_TYPE == 'GANACHE'):
            tx_hash = users.functions.deleteUser(id).transact()
        else:
            nonce = w3.eth.get_transaction_count(w3.eth.defaultAccount)
            tx = users.functions.deleteUser(id).buildTransaction({
                'nonce': nonce,
            })
            signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)
        return jsonify({"result": "Succesfull"}), 200
    except ContractLogicError as err:
        return jsonify({"error": str(err).split(': ')[-1]}), 422
    except ValueError as err:
        return jsonify({"error": err.args[0]['message']}), 422
    except BadFunctionCallOutput as err:
        return jsonify({"error": str(err)}), 422

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)