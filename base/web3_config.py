from web3 import Web3
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Check connection
assert w3.is_connected()

# Contract address (YOUR deployed one)
contract_address = ""

# Load ABI (copy from Remix)
with open("base/PensionSystemABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=abi)

# Owner account (from Ganache)
owner_address = w3.eth.accounts[0]

# Private key from Ganache (⚠️ dev only)
private_key = ""
