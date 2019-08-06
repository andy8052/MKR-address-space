import json, web3
from urllib.request import Request, urlopen
from web3 import Web3, WebsocketProvider

def calc():
    with open('erc20.json') as abi_json:
        tokenABI = json.load(abi_json)

    with open('data.json') as data_json:
        data = json.load(data_json)

    web3 = Web3(Web3.WebsocketProvider("wss://parity0.mainnet.makerfoundation.com:8546"))

    MKR_address = Web3.toChecksumAddress('0xc66ea802717bfb9833400264dd12c2bceaa34a6d')
    MKR_contract = web3.eth.contract(abi=tokenABI, address=MKR_address)

    block = int(data["block"])
    balance = 0
    counter = 0

    for guy in data["people"]:
        counter += 1
        balance += MKR_contract.functions.balanceOf(Web3.toChecksumAddress(guy)).call(block_identifier=block)
        print("Total balance is " + str(balance) + " -- " + str(counter) + "/" + str(len(data["people"])))

    return balance


calc()