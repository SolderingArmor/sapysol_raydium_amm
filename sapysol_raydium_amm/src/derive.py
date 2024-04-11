#!/usr/bin/python
# =============================================================================
#
#  ######     ###    ########  ##    ##  ######   #######  ##       
# ##    ##   ## ##   ##     ##  ##  ##  ##    ## ##     ## ##       
# ##        ##   ##  ##     ##   ####   ##       ##     ## ##       
#  ######  ##     ## ########     ##     ######  ##     ## ##       
#       ## ######### ##           ##          ## ##     ## ##       
# ##    ## ##     ## ##           ##    ##    ## ##     ## ##       
#  ######  ##     ## ##           ##     ######   #######  ########
#
# =============================================================================
#
# SuperArmor's Python Solana library.
# (c) SuperArmor
#
# module: Raydium derives
#
# =============================================================================
# 
from solana.rpc.api import Client, Pubkey, Keypair, Commitment
from .constants     import RAYDIUM_LIQUIDITY_POOL_V4 as PROGRAM_ID, RAYDIUM_SERUM_PROGAM_ID as SERUM_PROGRAM_ID
import contextlib

# =============================================================================
# 
def _DeriveLiquidityV4_Common(marketID: Pubkey, paramName: str) -> tuple[Pubkey, int]:
    return Pubkey.find_program_address(seeds      = [bytes(PROGRAM_ID),
                                                     bytes(marketID ),
                                                     bytes(paramName, "utf-8"),
                                                    ], 
                                       program_id = PROGRAM_ID)

# =============================================================================
# 
def DeriveAssociatedMarketAuthority(marketID: Pubkey, programID: Pubkey=SERUM_PROGRAM_ID) -> tuple[Pubkey, int]:
    seeds  = bytes(marketID)
    nonce  = 0
    pubkey = None
    while nonce < 100:
        try:
            # Buffer.alloc(7) nonce u64 equivalent in Python is creating a bytes array of length 7
            seeds_with_nonce = [seeds, bytes([nonce]), bytes(7)]
            pubkey = Pubkey.create_program_address(seeds=seeds_with_nonce, program_id=programID)
        except:
            nonce += 1
            continue
        return (pubkey, nonce)
    # If nonce was not found within the limit
    raise ValueError('Unable to find a viable program address nonce', {
        'programID': programID,
        'marketID':  marketID,
    })

# =============================================================================
# 
def DeriveLiquidityV4AssociatedAuthority(programID: Pubkey=PROGRAM_ID) -> Pubkey:
    seed = bytes([97, 109, 109, 32, 97, 117, 116, 104, 111, 114, 105, 116, 121])
    return Pubkey.find_program_address(seeds      = [seed], 
                                       program_id = programID)[0]

# =============================================================================
# 
def DeriveLiquidityV4AssociatedID(marketID: Pubkey) -> Pubkey:
    return _DeriveLiquidityV4_Common(marketID=marketID, paramName="amm_associated_seed")[0]

def DeriveLiquidityV4AssociatedBaseVault(marketID: Pubkey) -> Pubkey:
    return _DeriveLiquidityV4_Common(marketID=marketID, paramName="coin_vault_associated_seed")[0]

def DeriveLiquidityV4AssociatedQuoteVault(marketID: Pubkey) -> Pubkey:
    return _DeriveLiquidityV4_Common(marketID=marketID, paramName="pc_vault_associated_seed")[0]

def DeriveLiquidityV4AssociatedLpMint(marketID: Pubkey) -> Pubkey:
    return _DeriveLiquidityV4_Common(marketID=marketID, paramName="lp_mint_associated_seed")[0]

def DeriveLiquidityV4AssociatedLpVault(marketID: Pubkey) -> Pubkey:
    return _DeriveLiquidityV4_Common(marketID=marketID, paramName="temp_lp_token_associated_seed")[0]

def DeriveLiquidityV4AssociatedTargetOrders(marketID: Pubkey) -> Pubkey:
    return _DeriveLiquidityV4_Common(marketID=marketID, paramName="target_associated_seed")[0]

def DeriveLiquidityV4AssociatedWithdrawQueue(marketID: Pubkey) -> Pubkey:
    return _DeriveLiquidityV4_Common(marketID=marketID, paramName="withdraw_associated_seed")[0]

def DeriveLiquidityV4AssociatedOpenOrders(marketID: Pubkey) -> Pubkey:
    return _DeriveLiquidityV4_Common(marketID=marketID, paramName="open_order_associated_seed")[0]

# =============================================================================
# 
def DeriveLiquidityV4AssociatedConfigId() -> Pubkey:
    return Pubkey.find_program_address(seeds      = [b"amm_config_account_seed"], 
                                       program_id = PROGRAM_ID)[0]

# =============================================================================
# 
