from eth_account.messages import encode_defunct
from eth_account import Account
import requests
from web3 import Web3
import requests

import time

web3 = Web3()

def read_addresses(filename):
    addresses = []
    with open(filename, "r") as file:
        for line in file:
            address, private_key = line.strip().split("----")
            addresses.append((address, private_key))
    return addresses

def ethsign(privatekey,time):
    message = "Greetings from Avail!\n\nSign this message to check your eligibility. This signature will not cost you any fees.\n\nTimestamp: " + time
    message = encode_defunct(text=message)
    signed_message = web3.eth.account.sign_message(message, private_key=privatekey)
    sign = web3.to_hex(signed_message.signature)
    return sign

def post(address,privatekey):
    timestamp = int(time.time())

    sign = ethsign(privatekey,str(timestamp))

    headers = {"Content-Type": "application/json"}

    data = {"account": address,"type": "ETHEREUM","timestamp": timestamp,"signedMessage": sign}

    response = requests.post("https://claim-api.availproject.org/check-rewards", json=data, headers=headers)

    json_data = response.json()

    message = json_data["message"]

    return message



def main(filename):
    addresses = read_addresses(filename)
    for address, private_key in addresses:
        message = post(address, private_key)
        print(f"钱包地址: {address}, 结果: {message}")


main("addresses.txt")

