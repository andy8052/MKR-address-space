import json, web3
from urllib.request import Request, urlopen
from web3 import Web3, WebsocketProvider

def sort_by_balance(d):
    '''a helper function for sorting'''
    return d['balance']

def calc():
    with open('erc20.json') as abi_json:
        tokenABI = json.load(abi_json)

    with open('data.json') as data_json:
        data = json.load(data_json)

    web3 = Web3(Web3.WebsocketProvider(""))

    MKR_address = Web3.toChecksumAddress('0xc66ea802717bfb9833400264dd12c2bceaa34a6d')
    MKR_contract = web3.eth.contract(abi=tokenABI, address=MKR_address)

    block = int(data["block"])
    balance = 0
    counter = 0

    balances = []

    for guy in data["people"]:
        counter += 1
        print(str(counter) + " of " + str(len(data["people"])))
        balance = MKR_contract.functions.balanceOf(Web3.toChecksumAddress(guy)).call(block_identifier=block)
        temp = {}
        temp["address"] = Web3.toChecksumAddress(guy)
        temp["balance"] = balance
        balances.append(temp)

    with open('balance-list.json', 'w') as outfile:  
        json.dump(sorted(balances, key=sort_by_balance, reverse=True), outfile)


calc()