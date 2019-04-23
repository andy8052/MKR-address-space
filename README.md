# MKR-address-space
A Google Cloud Function to keep track of the addresses that have touched MKR tokens

You can test this function by going to [this link](https://us-central1-causal-ratio-238015.cloudfunctions.net/MKR-holders). Please don't spam it as it will probably crash.

## Running locally
You have a few options here:
- If you want to start from scratch, delete the `people` list and update the `block` variable to whatever you want to start from (I recommend `block 4620855` since that is where MKR was created)
- Otherwise, you can trust data.json and just run `token-snapshot.py`. This will update `data.json` to the latest block

You will need to add a websocket address to the python files. 

TODO - move the address to an environment variable

From there, you can run `balance-check.py` to verify the MKR total is 1,000,000 MKR. 
