import json, web3
from web3 import Web3, WebsocketProvider

def send():
    with open('erc20.json') as abi_json:
        tokenABI = json.load(abi_json)

    with open('data.json') as data_json:
        data = json.load(data_json)

    with open('bad.json') as bad_json:
        bad = json.load(bad_json)

    # Your address and pk that hold all of the new MKR
    address = Web3.toChecksumAddress('<address>')
    pk = '<your private key for above address>'
    dev = Web3.toChecksumAddress('<address of the dev fund>')

    # This is only for testing. We pull in balances from mainnet and redistribute on Goerli
    # For a real deploy you would only need one
    web3 = Web3(Web3.WebsocketProvider("<testnet wss url>"))
    web3Mainnet = Web3(Web3.WebsocketProvider("<mainnet wss url>"))

    # TODO figure out why the web3py call for nonce is broken
    nonce = 3048

    # The mainnet MKR address
    oldMKR = Web3.toChecksumAddress('0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2')
    # Your testnet deployed MKR address
    newMKR = Web3.toChecksumAddress('<MKR address>')

    old = web3Mainnet.eth.contract(abi=tokenABI, address=oldMKR)
    new = web3.eth.contract(abi=tokenABI, address=newMKR)

    block = int(data["block"])
    total = 0

    # Send the tokens to all users
    # Keeps a running total so we can make sure it does not fail

    for guy in data["people"]:
        if guy in bad["people"]:
            continue

        amt = old.functions.balanceOf(Web3.toChecksumAddress(guy)).call(block_identifier=block)

        if amt != 0:
            txn = new.functions.transfer(
                Web3.toChecksumAddress(guy),
                amt,
            ).buildTransaction({
                'chainId': 5,
                'gas': 70000,
                'gasPrice': Web3.toWei('2', 'gwei'),
                'nonce': nonce,
            })
            sgn = web3.eth.account.signTransaction(txn, private_key=pk)   

            web3.eth.sendRawTransaction(sgn.rawTransaction)   

            total += amt
            print("Sent " + str(amt) + " MKR to " + Web3.toChecksumAddress(guy) + " || " + str(total) + " MKR Total")

            nonce += 1

    # Handle any tokens that are being stripped of bad actors in the system
    # TODO some cool redistribute logic instead of just sending to the dev fund

    takenMKR = badGuysTokens(bad, old, block)

    if (bad["action"] == "redistribute"):
        txn = new.functions.transfer(
            Web3.toChecksumAddress(dev),
            takenMKR,
        ).buildTransaction({
            'chainId': 5,
            'gas': 70000,
            'gasPrice': Web3.toWei('2', 'gwei'),
            'nonce': nonce,
        })
        sgn = web3.eth.account.signTransaction(txn, private_key=pk)   

        web3.eth.sendRawTransaction(sgn.rawTransaction)   

        total += takenMKR
        print("Sent " + str(takenMKR) + " MKR to " + Web3.toChecksumAddress(dev) + " || " + str(total) + " MKR Total")

    if (bad["action"] == "burn"):
        txn = new.functions.burn(
            takenMKR,
        ).buildTransaction({
            'chainId': 5,
            'gas': 70000,
            'gasPrice': Web3.toWei('2', 'gwei'),
            'nonce': nonce,
        })
        sgn = web3.eth.account.signTransaction(txn, private_key=pk)   

        web3.eth.sendRawTransaction(sgn.rawTransaction)   

        total += takenMKR
        print("Burned " + str(takenMKR) + " MKR || " + str(total) + " MKR Total")

def badGuysTokens(bad, old, block):
    taken = 0
    for guy in bad["people"]:
        amt = old.functions.balanceOf(Web3.toChecksumAddress(guy)).call(block_identifier=block)
        taken += amt

    return taken

send()