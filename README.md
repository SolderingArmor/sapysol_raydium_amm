# sapysol_raydium_amm

`sapysol` Raydium AMM V4 direct swap implementation. Based on JavaScript from [Raydium SDK](https://github.com/raydium-io/raydium-sdk), written from scratch.

`sapysol_raydium_amm` fetches information from Solana blockchain and doesn't rely on Raydium public web APIs, that means ig you know pool address you can start trading right away without the need to wait for the Raydium pool cache to be updated.

WARNING! `sapysol_raydium_amm` is currently in `alpha` version, so, bugs, lack of tests and descriptions are expected. Some things may not work, future versions may bring breaking changes.

# Installation

```sh
pip install sapysol
```

Note: Requires Python >= 3.10.

# Usage

```py
# Raydium AMM Swap, WSOL for MEW example
#
from solana.rpc.api      import Client
from sapysol             import *
from sapysol.token_cache import *
from typing              import List
from sapysol_raydium_amm import *

SetupLogging()

connection: Client  = Client("https://api.mainnet-beta.solana.com")
payer:      Keypair = MakeKeypair("/path/to/keypair.json")
POOL_ID:    Pubkey  = MakePubkey("879F697iuDJGMevRkRcnW21fcXiAeLJK1ffsw2ATebce") # MEW-WSOL AMM Pool ID

amm: SapysolRaydiumAMM = SapysolRaydiumAMM.FromPoolAddress(connection=connection, poolAddress=POOL_ID)
ixList = amm.GetSwapInstruction(walletAddress  = MakePubkey(payer),
                                tokenFrom      = WSOL,
                                tokenTo        = MEW,
                                amountIn       = 0.01,
                                inLamports     = False,
                                txComputePrice = 10_000)
tx: SapysolTx = SapysolTx(connection = connection, 
                          payer      = payer, 
                          txParams   = SapysolTxParams(maxSecondsPerTx=60, sleepBetweenRetry=1))
tx.FromInstructionsLegacy(ixList)
tx.Sign().SendAndWait()
```

But if you wanto FKIN SNIPE the pool that was not created yet, knowing only OpenBook Market ID, I got you! This library can pre-calculate all needed addresses from Market ID only! Transactions will fail until the actual pool is created of course, but you may be one of the first ones to make a buy.

```py
# Raydium AMM Swap, WSOL for MEW example
#
from solana.rpc.api      import Client
from sapysol             import *
from sapysol.token_cache import *
from typing              import List
from sapysol_raydium_amm import *

SetupLogging()

connection: Client  = Client("https://api.mainnet-beta.solana.com")
payer:      Keypair = MakeKeypair("/path/to/keypair.json")
MARKET_ID:  Pubkey  = MakePubkey("CujsiQUzNUPKTADPQ67XKJKbaVo4KpzEXvNPp1gXzQKH") # MEW-WSOL Market ID

amm: SapysolRaydiumAMM = SapysolRaydiumAMM.FromMarketAddress(connection=connection, marketAddress=POOL_ID)
ixList = amm.GetSwapInstruction(walletAddress  = MakePubkey(payer),
                                tokenFrom      = WSOL,
                                tokenTo        = MEW,
                                amountIn       = 0.01,
                                inLamports     = False,
                                txComputePrice = 10_000)
tx: SapysolTx = SapysolTx(connection = connection, 
                          payer      = payer, 
                          txParams   = SapysolTxParams(maxSecondsPerTx=60, sleepBetweenRetry=1))
tx.FromInstructionsLegacy(ixList)
tx.Sign().SendAndWait()
```


TODO

# Contributing

All contributions are welcome! Although the devil is in the details:

One of the main requirements is to **keep the same coding style** for all future changes.

If you want to help the project and implement adding/removing liquidity, etc - you are welcome!

# Tests

TODO

# Contact

[Telegram](https://t.me/sapysol)

Donations: `SAxxD7JGPQWqDihYDfD6mFp7JWz5xGrf9RXmE4BJWTS`

# Disclaimer

### Intended Purpose and Use
The Content is provided solely for educational, informational, and general purposes. It is not intended for use in making any business, investment, or legal decisions. Although every effort has been made to keep the information up-to-date and accurate, no representations or warranties, express or implied, are made regarding the completeness, accuracy, reliability, suitability, or availability of the Content.

### Opinions and Views
The views and opinions expressed herein are those of Anton Platonov and do not necessarily reflect the official policy, position, or views of any other agency, organization, employer, or company. These views are subject to change, revision, and rethinking at any time.

### Third-Party Content and Intellectual Property
Some Content may include or link to third-party materials. The User agrees to respect all applicable intellectual property laws, including copyrights and trademarks, when engaging with this Content.

### Amendments
Chintan Gurjar reserves the right to update or change this disclaimer at any time without notice. Continued use of the Content following modifications to this disclaimer will constitute acceptance of the revised terms.