import sys
import os
import random
from web3 import Web3
from decimal import Decimal
import json

# Set up Web3 connection
KAIA_RPC_URL = "https://public-en.node.kaia.io"
web3 = Web3(Web3.HTTPProvider(KAIA_RPC_URL))

if not web3.is_connected():
    raise ConnectionError("Failed to connect to Kaia chain.")

# Constants
KAWAII_ABI = json.loads('''[
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "name",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "symbol",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "initialSupply",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "owner",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "spender",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "value",
          "type": "uint256"
        }
      ],
      "name": "Approval",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "value",
          "type": "uint256"
        }
      ],
      "name": "Transfer",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "owner",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "spender",
          "type": "address"
        }
      ],
      "name": "allowance",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "spender",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "approve",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "balanceOf",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "decimals",
      "outputs": [
        {
          "internalType": "uint8",
          "name": "",
          "type": "uint8"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "spender",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "subtractedValue",
          "type": "uint256"
        }
      ],
      "name": "decreaseAllowance",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "spender",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "addedValue",
          "type": "uint256"
        }
      ],
      "name": "increaseAllowance",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "name",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "recipient",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "safeTransfer",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "recipient",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        },
        {
          "internalType": "bytes",
          "name": "_data",
          "type": "bytes"
        }
      ],
      "name": "safeTransfer",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "sender",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "recipient",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "safeTransferFrom",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "sender",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "recipient",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        },
        {
          "internalType": "bytes",
          "name": "_data",
          "type": "bytes"
        }
      ],
      "name": "safeTransferFrom",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes4",
          "name": "interfaceId",
          "type": "bytes4"
        }
      ],
      "name": "supportsInterface",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "symbol",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "totalSupply",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "transfer",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "transferFrom",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]''')  # Replace with actual ABI

WKAIA_ABI = json.loads('''[
    {
        "constant": true,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_spender",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_from",
                "type": "address"
            },
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            },
            {
                "name": "_spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "payable": true,
        "stateMutability": "payable",
        "type": "fallback"
    },
    {
        "constant": false,
        "inputs": [],
        "name": "deposit",
        "outputs": [],
        "payable": true,
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "wad",
                "type": "uint256"
            }
        ],
        "name": "withdraw",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": true,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": false,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": true,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": false,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    }
]
''')

POOL_ABI = '''
[
    {"constant":true,"inputs":[],"name":"getReserves","outputs":[{"name":"reserve0","type":"uint256"},{"name":"reserve1","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant": false, "inputs": [{"name": "to", "type": "address"}, {"name": "value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"},
    {"constant": false, "inputs": [], "name": "sync", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"constant": false, "inputs": [{"name": "amount0Out", "type": "uint256"}, {"name": "amount1Out", "type": "uint256"}, {"name": "to", "type": "address"}, {"name": "data", "type": "bytes"}], "name": "swap", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"constant":false,"inputs":[{"name":"amountIn","type":"uint256"},{"name":"amountOutMin","type":"uint256"},{"name":"path","type":"address[]"},{"name":"to","type":"address"},{"name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"name":"amounts","type":"uint256[]"}],"payable":false,"stateMutability":"nonpayable","type":"function"}
]
'''
# {"constant":false,"inputs":[{"name":"amountIn","type":"uint256"},{"name":"amountOutMin","type":"uint256"},{"name":"path","type":"address[]"},{"name":"to","type":"address"},{"name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[],"payable":false,"stateMutability":"nonpayable",
ROUTER_ABI = json.loads('''
[
    {
        "inputs": [
            {
                "name": "amountOutMin",
                "type": "uint256"
            },
            {
                "name": "path",
                "type": "address[]"
            },
            {
                "name": "to",
                "type": "address"
            },
            {
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapExactETHForTokens",
        "outputs": [],
        "payable": true,
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountOutMin",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapExactTokensForTokens",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "spender",
                "type": "address"
            },
            {
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
''')


GAS_PRICE = web3.to_wei(Decimal("0.000000027"), 'ether')
KAWAII_TOKEN_ADDRESS = web3.to_checksum_address("0x4159df9507Ed52d20Ae7fD652A955d16140f2d2a")
WKAIA_TOKEN_ADDRESS = WKAIA_CONTRACT_ADDRESS = web3.to_checksum_address("0x19aac5f612f524b754ca7e7c41cbfa2e981a4432")
POOL_ADDRESS = web3.to_checksum_address("0xc9575eaca554f5926036a7856ae4e48925c389cb")
SMART_ROUTER_ADDRESS = web3.to_checksum_address("0x5ea3e22c41b08dd7dc7217549939d987ed410354")
wkaia_token = wkaia_contract = web3.eth.contract(address=WKAIA_TOKEN_ADDRESS, abi=WKAIA_ABI)
kawaii_token = web3.eth.contract(address=KAWAII_TOKEN_ADDRESS, abi=KAWAII_ABI)
pool_contract = web3.eth.contract(address=POOL_ADDRESS, abi=POOL_ABI)
router_contract = web3.eth.contract(address=SMART_ROUTER_ADDRESS, abi=ROUTER_ABI)


# Load wallets from file
kaia_wallets_file = "kaia_wallets.txt"
if not os.path.exists(kaia_wallets_file):
    raise FileNotFoundError(f"{kaia_wallets_file} not found.")

with open(kaia_wallets_file, "r") as f:
    wallet_lines = f.readlines()

wallets = []
for i in range(0, len(wallet_lines), 4):
    address = wallet_lines[i + 1].split("Address: ")[1].strip()
    private_key = wallet_lines[i + 2].split("Private Key: ")[1].strip()
    wallets.append({"address": address, "private_key": private_key})

# Get number of wallets to load from command line arguments
if len(sys.argv) < 3:
    raise ValueError("Usage: python wallet_purchase_script.py <number_of_wallets> <target_kawaii_tokens>")

num_wallets = int(sys.argv[1])
if num_wallets > len(wallets):
    raise ValueError("Requested number of wallets exceeds available wallets.")

target_tokens = Decimal(sys.argv[2])
if target_tokens <= 0:
    raise ValueError("Target number of KAWAII tokens must be greater than 0.")

# Randomly select wallets
selected_wallets = random.sample(wallets, num_wallets)

# Assign random number of tokens to each selected wallet
def assign_tokens_to_wallets(target_tokens, wallets):
    num_wallets = len(wallets)
    base_allocation = Decimal(target_tokens / num_wallets)
    while True:
        token_allocations = [round(base_allocation + Decimal(random.uniform(-float(base_allocation) * 0.5, float(base_allocation) * 0.5)), 8) for _ in wallets]
        if sum(token_allocations) >= target_tokens and sum(token_allocations) <= Decimal(target_tokens * Decimal(1.1)):
            return token_allocations

assigned_tokens = assign_tokens_to_wallets(target_tokens, selected_wallets)


def get_kawaii_to_kaia_ratio():
    # Retrieve the current reserves of KAWAII and KAIA from the pool contract using a function call
    try:
        reserves = pool_contract.functions.getReserves().call()
        reserve_kaia = Decimal(reserves[0])
        reserve_kawaii = Decimal(reserves[1])

        # Calculate the price ratio of KAWAII to KAIA
        if reserve_kawaii == 0 or reserve_kaia == 0:
            raise ValueError("Invalid pool reserves, cannot calculate ratio.")

        return reserve_kaia / reserve_kawaii
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve reserves: {e}")


def approve_kawaii(kaia_needed, wallet_address, private_key, nonce):
    try:
        current_allowance = kawaii_token.functions.allowance(wallet_address, SMART_ROUTER_ADDRESS).call()
        if current_allowance < int(kaia_needed * (10 ** 18)):
            # Approve Router
            approve_router_tx = kawaii_token.functions.approve(SMART_ROUTER_ADDRESS, int(kaia_needed * (10 ** 18))).build_transaction({
                'chainId': web3.eth.chain_id,
                'gas': 100000,
                'gasPrice': GAS_PRICE,
                'nonce': nonce,
            })
            signed_approve_router_tx = web3.eth.account.sign_transaction(approve_router_tx, private_key)
            web3.eth.send_raw_transaction(signed_approve_router_tx.raw_transaction)
            print(f"Approved Smart Router with {kaia_needed} KAIA from wallet {wallet_address}.")
            nonce += 1
        else:
            print(f"Router already approved for {wallet_address}.")
    except Exception as e:
        print(f"Approval check/transaction failed for {wallet_address}: {e}")
        return
    
# Purchase tokens from pool for each selected wallet
print(assigned_tokens)

def batch_transaction(wallet, kaia_needed, amount_to_purchase):
    wallet_address = wallet['address']
    private_key = wallet['private_key']
    nonce = web3.eth.get_transaction_count(wallet_address)

    # Approve Smart Router
    # approve_router_tx = kawaii_token.functions.approve(SMART_ROUTER_ADDRESS, int(amount_to_purchase * (10 ** 18))).build_transaction({
    #     'chainId': web3.eth.chain_id,
    #     'gas': 200000,
    #     'gasPrice': GAS_PRICE,
    #     'nonce': nonce,
    # })
    # signed_approve_router_tx = web3.eth.account.sign_transaction(approve_router_tx, private_key)
    # web3.eth.send_raw_transaction(signed_approve_router_tx.raw_transaction)
    # print(f"Approved Smart Router with {amount_to_purchase} KAWAII tokens from wallet {wallet_address}.")
    # nonce += 1

    # Check if already approved
    # approve_kawaii(kaia_needed, wallet_address, private_key, nonce)

    # Approve Pool
    # approve_pool_tx = kawaii_token.functions.approve(POOL_ADDRESS, int(amount_to_purchase * (10 ** 18))).build_transaction({
    #     'chainId': web3.eth.chain_id,
    #     'gas': 200000,
    #     'gasPrice': GAS_PRICE,
    #     'nonce': nonce,
    # })
    # signed_approve_pool_tx = web3.eth.account.sign_transaction(approve_pool_tx, private_key)
    # web3.eth.send_raw_transaction(signed_approve_pool_tx.raw_transaction)
    # print(f"Approved Pool with {amount_to_purchase} KAWAII tokens from wallet {wallet_address}.")
    # nonce += 1

    path = [WKAIA_CONTRACT_ADDRESS, KAWAII_TOKEN_ADDRESS] 
    # swap_tx = router_contract.functions.swapExactTokensForTokens(
    #     int(kaia_needed * 10 ** 18), 0, path, wallet_address, int(web3.eth.get_block('latest')['timestamp']) + 30
    # ).build_transaction({
    #     'chainId': web3.eth.chain_id,
    #     'from': wallet_address,
    #     'nonce': nonce,
    #     'gas': 300000,
    #     'gasPrice': GAS_PRICE,
    # })

    swap_tx = router_contract.functions.swapExactETHForTokens(
        int(kaia_needed * 10 ** 18), path, wallet_address, int(web3.eth.get_block('latest')['timestamp']) + 30
    ).build_transaction({
        'chainId': web3.eth.chain_id,
        'from': wallet_address,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': GAS_PRICE,
    })

    # Purchase tokens from pool using Swap function
    # swap_tx = pool_contract.functions.swapExactTokensForTokens(
    #     int(kaia_needed), 0, path, wallet_address, int(web3.eth.get_block('latest')['timestamp']) + 30
    # ).build_transaction({
    #     'chainId': web3.eth.chain_id,
    #     'gas': 300000,
    #     'gasPrice': GAS_PRICE,
    #     'nonce': nonce,
    # })

    # Sign and send the transaction
    signed_swap_tx = web3.eth.account.sign_transaction(swap_tx, private_key)
    web3.eth.send_raw_transaction(signed_swap_tx.raw_transaction)
    print(f"Purchased {amount_to_purchase} KAWAII tokens for {kaia_needed} KAIA from pool with wallet {wallet_address}.")

    
# Execute batch transaction for each selected wallet
for wallet, tokens_to_purchase in zip(selected_wallets, assigned_tokens):
    # Calculate KAIA needed
    price_ratio = get_kawaii_to_kaia_ratio()
    kaia_needed = tokens_to_purchase * price_ratio

    # Check if wallet has enough KAIA
    wallet_balance = web3.eth.get_balance(wallet['address'])
    if wallet_balance < kaia_needed:
        print(f"Wallet {wallet['address']} does not have enough KAIA tokens.")
        continue

    # Execute batch transaction
    batch_transaction(wallet, kaia_needed, tokens_to_purchase)
