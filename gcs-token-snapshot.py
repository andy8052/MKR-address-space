import json, web3
from google.cloud import storage
from web3 import Web3, WebsocketProvider

def people(request):
            
    client = storage.Client()
    bucket = client.get_bucket('people-json')
    dataBlob = bucket.get_blob('data.json')
    erc20Blob = bucket.get_blob('erc20.json')
    data = json.loads(dataBlob.download_as_string())
    erc20 = json.loads(erc20Blob.download_as_string())
    
    web3 = Web3(Web3.WebsocketProvider("<your websocket address>"))
    MKR_address = Web3.toChecksumAddress('0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2')
    MKR_contract = web3.eth.contract(abi=erc20, address=MKR_address)
    
    people = data["people"]
    fromBlock = int(data["block"])
    tempTo = fromBlock + 1000
    latestBlock = web3.eth.getBlock('latest').number
    toBlock = tempTo if tempTo < latestBlock else latestBlock

    events = MKR_contract.events.Transfer().createFilter(fromBlock=fromBlock, toBlock=toBlock).get_all_entries()

    for event in events:
        address = event["args"]["to"]
        if address not in people:
            people.append(address)
            print("Added address " + str(address))

    while toBlock < latestBlock:

        fromBlock = toBlock
        tempTo = fromBlock + 1000
        toBlock = tempTo if tempTo < latestBlock else latestBlock

        events = MKR_contract.events.Transfer().createFilter(fromBlock=fromBlock, toBlock=toBlock).get_all_entries()

        for event in events:
            address = event["args"]["to"]
            if address not in people:
                people.append(address)
                print("Added address " + str(address))

    data["block"] = toBlock
    data["people"] = people
    
    dataBlob.upload_from_string(json.dumps(data))

    return json.dumps(data)