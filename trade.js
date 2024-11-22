require("dotenv").config()
const ethers = require('ethers')
const {ChainId, CurrencyAmount, Token, TokenAmount, Fetcher, validateAndParseAddress, WNATIVE, Pair, Route, Trade, TradeType, Percent} = 
require('@pancakeswap-libs/sdk');
const {Web3} = require('web3');
const { Transaction } = require('@ethereumjs/tx');
const Common = require('@ethereumjs/common').default;
const { encodeFunctionData, Hex, Address } = require('viem');
const invariant = require('tiny-invariant');
// const { address: admin } = web3.eth.accounts.wallet.add(process.env.PRIVATE_KEY)

const fs = require('fs');
const path = require('path');

// Set up Web3 connection
const KAIA_RPC_URLS = [
  "https://kaia.blockpi.network/v1/rpc/public",
  "https://public-en.node.kaia.io"
];

let web3 = null;
let provider = null;
for (const rpcUrl of KAIA_RPC_URLS) {
  web3 = new Web3(rpcUrl);
  if (web3 && web3.eth.net.isListening()) {
    provider = new ethers.JsonRpcProvider(rpcUrl);
    break;
  }
}



if (!web3) {
  throw new Error("Failed to connect to any of the provided Kaia RPC URLs.");
}

// Constants
const KAWAII_TOKEN_ADDRESS = "0x4159df9507Ed52d20Ae7fD652A955d16140f2d2a";
const SMART_ROUTER_ADDRESS = "0x5ea3e22c41b08dd7dc7217549939d987ed410354";
const WKAIA_TOKEN_ADDRESS = "0x19aac5f612f524b754ca7e7c41cbfa2e981a4432";
const POOL_ADDRESS = "0xc9575eaca554f5926036a7856ae4e48925c389cb";
const GAS_PRICE = web3.utils.toWei("0.000000027", 'ether');
const POOL_FEE = 2500;  // 0.25% fee tier

// Load wallets from file
const kaiaWalletsFile = "kaia_wallets.txt";
if (!fs.existsSync(kaiaWalletsFile)) {
  throw new Error(`${kaiaWalletsFile} not found.`);
}

const walletLines = fs.readFileSync(kaiaWalletsFile, 'utf-8').split('\n');
let wallets = [];
for (let i = 0; i < walletLines.length; i += 4) {
  const address = walletLines[i + 1].split("Address: ")[1].trim();
  const privateKey = walletLines[i + 2].split("Private Key: ")[1].trim();
  wallets.push({ address, privateKey });
}

// Get number of wallets to load from command line arguments
if (process.argv.length < 4) {
  throw new Error("Usage: node wallet_purchase_script.js <number_of_wallets> <target_kawaii_tokens>");
}

const numWallets = parseInt(process.argv[2], 10);
if (numWallets > wallets.length) {
  throw new Error("Requested number of wallets exceeds available wallets.");
}

const targetTokens = parseFloat(process.argv[3]);
if (targetTokens <= 0) {
  throw new Error("Target number of KAWAII tokens must be greater than 0.");
}

// Randomly select wallets
const selectedWallets = wallets.sort(() => 0.5 - Math.random()).slice(0, numWallets);

// Assign random number of tokens to each selected wallet
function assignTokensToWallets(targetTokens, wallets) {
  const numWallets = wallets.length;
  const baseAllocation = targetTokens / numWallets;
  console.log('wallet: ', numWallets, ' allo: ', baseAllocation)
  while (true) {
    const tokenAllocations = wallets.map(() =>
      parseFloat((baseAllocation + (Math.random() - 0.5) * baseAllocation * 0.5).toFixed(8))
    );
    const totalAllocated = tokenAllocations.reduce((acc, value) => acc + value, 0);
    if (totalAllocated >= targetTokens && totalAllocated <= targetTokens * 1.01) {
      return tokenAllocations;
    }
  }
}

const assignedTokens = assignTokensToWallets(targetTokens, selectedWallets);
console.log(targetTokens)
selectedWallets.forEach(wallet => console.log(wallet.address))

const POOL_ABI = `
[
    {"constant":true,"inputs":[],"name":"getReserves","outputs":[{"name":"reserve0","type":"uint256"},{"name":"reserve1","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant": false, "inputs": [{"name": "to", "type": "address"}, {"name": "value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"},
    {"constant": false, "inputs": [], "name": "sync", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"constant": false, "inputs": [{"name": "amount0Out", "type": "uint256"}, {"name": "amount1Out", "type": "uint256"}, {"name": "to", "type": "address"}, {"name": "data", "type": "bytes"}], "name": "swap", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"constant":false,"inputs":[{"name":"amountIn","type":"uint256"},{"name":"amountOutMin","type":"uint256"},{"name":"path","type":"address[]"},{"name":"to","type":"address"},{"name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"name":"amounts","type":"uint256[]"}],"payable":false,"stateMutability":"nonpayable","type":"function"}
]
`;

const ROUTER_ABI = JSON.parse(`
    [{
    "inputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "tokenIn",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "tokenOut",
            "type": "address"
          },
          {
            "internalType": "uint24",
            "name": "fee",
            "type": "uint24"
          },
          {
            "internalType": "address",
            "name": "recipient",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "amountOut",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "amountInMaximum",
            "type": "uint256"
          },
          {
            "internalType": "uint160",
            "name": "sqrtPriceLimitX96",
            "type": "uint160"
          }
        ],
        "internalType": "struct IV3SwapRouter.ExactOutputSingleParams",
        "name": "params",
        "type": "tuple"
      }
    ],
    "name": "exactOutputSingle",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "amountIn",
        "type": "uint256"
      }
    ],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {
            "internalType": "bytes",
            "name": "path",
            "type": "bytes"
          },
          {
            "internalType": "address",
            "name": "recipient",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "amountOut",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "amountInMaximum",
            "type": "uint256"
          }
        ],
        "internalType": "struct IV3SwapRouter.ExactOutputParams",
        "name": "params",
        "type": "tuple"
      }
    ],
    "name": "exactOutput",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "amountIn",
        "type": "uint256"
      }
    ],
    "stateMutability": "payable",
    "type": "function"
  },
        {
            "constant": false,
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
        }
    ]
    `);    

const swapRouter = new web3.eth.Contract(ROUTER_ABI, SMART_ROUTER_ADDRESS)

// Get KAWAII to KAIA ratio
async function getKawaiiToKaiaRatio() {
    const wallet = new ethers.Wallet(selectedWallets[0].privateKey, provider)
    const signer = wallet.connect(provider)
    try {
      const poolContract = new ethers.Contract(
        POOL_ADDRESS,
        POOL_ABI,
        signer
      )
      const reserves = await poolContract.getReserves();
      const reserveKaia = parseFloat(reserves.reserve0);
      const reserveKawaii = parseFloat(reserves.reserve1);
  
      if (reserveKaia === 0 || reserveKawaii === 0) {
        throw new Error("Invalid pool reserves, cannot calculate ratio.");
      }
  
      return reserveKaia / reserveKawaii;
    } catch (error) {
      throw new Error(`Failed to retrieve reserves: ${error.message}`);
    }
  }
  
// Batch transaction to Smart Router
async function batchTransaction(wallet, kaiaNeeded, amountToPurchase) {
    const walletAddress = wallet.address;
    const privateKey = wallet.privateKey;
  
    try {
      // Get current nonce
      let nonce = await web3.eth.getTransactionCount(walletAddress);

        const path = web3.eth.abi.encodeParameters(
            ['address', 'uint24', 'address'],
            [WKAIA_TOKEN_ADDRESS, POOL_FEE, KAWAII_TOKEN_ADDRESS]
        );

        const kaiaNeededBuffer = kaiaNeeded + 40
        const params = {
            tokenIn: WKAIA_TOKEN_ADDRESS,
            tokenOut: KAWAII_TOKEN_ADDRESS,
            fee: POOL_FEE,
            recipient: walletAddress,
            amountOut: web3.utils.toWei(amountToPurchase.toString(), 'ether'),
            amountInMaximum: web3.utils.toWei(kaiaNeededBuffer.toString(), 'ether'),
            sqrtPriceLimitX96: 0
        };
        const swapTx = swapRouter.methods.exactOutputSingle(params).encodeABI();

        var rawTransaction = {
            "from":walletAddress,
            "gasPrice": GAS_PRICE,
            "gasLimit":web3.utils.toHex(500000),
            "to":SMART_ROUTER_ADDRESS,
            "value": web3.utils.toWei(kaiaNeededBuffer.toString(), 'ether'),
            "data":swapTx,
            "nonce":nonce
        };

        // Sign the transaction
        const signedTx = await web3.eth.accounts.signTransaction(rawTransaction, privateKey);

        // Send the signed transaction
        const receipt = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);
        console.log("Transaction successful:", receipt);

        // var transaction = new Transaction.Tx(rawTransaction);
        // transaction.sign(privateKey);
        
        console.log(`Tx was mined in block: ${receipt.blockNumber}`)
        console.log(`Purchased ${amountToPurchase} KAWAII tokens for ${kaiaNeeded} KAIA from pool with wallet ${walletAddress}. Transaction hash: ${receipt.transactionHash}`);
        
    } catch (error) {
      console.error(`Error executing transaction for wallet ${walletAddress}: ${error.message}`);
      console.error(JSON.stringify(error));
    }
}

// Execute batch transaction for each selected wallet
(async () => {
    for (let i = 0; i < selectedWallets.length; i++) {
      const wallet = selectedWallets[i];
      const tokensToPurchase = assignedTokens[i];
  
      // Calculate KAIA needed
      const priceRatio = await getKawaiiToKaiaRatio();
      const kaiaNeeded = tokensToPurchase * priceRatio;
  
      // Check if wallet has enough KAIA
      const walletBalance = await web3.eth.getBalance(wallet.address);
      if (parseFloat(web3.utils.fromWei(walletBalance, 'ether')) < kaiaNeeded) {
        console.log(`Wallet ${wallet.address} does not have enough KAIA tokens.`);
        continue;
      }
  
      // Execute batch transaction
      await batchTransaction(wallet, kaiaNeeded, tokensToPurchase);
    }
  })();
