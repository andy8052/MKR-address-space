import json, web3
from web3 import Web3, WebsocketProvider

def new_holders():
    with open('erc20.json') as abi_json:
        tokenABI = json.load(abi_json)

    with open('data.json') as data_json:
        data = json.load(data_json)

    jump = 1000

    web3 = Web3(Web3.WebsocketProvider("<your websocket address>"))
    MKR_address = Web3.toChecksumAddress('0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2')
    MKR_contract = web3.eth.contract(abi=tokenABI, address=MKR_address)

    people = data["people"]
    fromBlock = int(data["block"])
    latestBlock = web3.eth.getBlock('latest').number
    tempTo = fromBlock + jump
    toBlock = tempTo if tempTo < latestBlock else latestBlock

    events = MKR_contract.events.Transfer().createFilter(fromBlock=fromBlock, toBlock=toBlock).get_all_entries()

    for event in events:
        address = Web3.toChecksumAddress(event["args"]["to"])
        if address not in people:
            people.append(address)

    while toBlock < latestBlock:

        print("AT BLOCK " + str(toBlock))

        fromBlock = toBlock
        tempTo = fromBlock + jump
        toBlock = tempTo if tempTo < latestBlock else latestBlock

        events = MKR_contract.events.Transfer().createFilter(fromBlock=fromBlock, toBlock=toBlock).get_all_entries()

        for event in events:
            address = Web3.toChecksumAddress(event["args"]["to"])
            if address not in people:
                people.append(address)

    data["block"] = toBlock
    data["people"] = people

    with open('data.json', 'w') as outfile:  
        json.dump(data, outfile)

new_holders()

#If you ever need/want to go from scratch, MKR was created at block 4620855