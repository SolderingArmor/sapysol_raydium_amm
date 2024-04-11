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
# module: Raydium layouts base
#
# =============================================================================
# 
import typing
import borsh_construct as borsh
from   dataclasses              import dataclass
from   solders.pubkey           import Pubkey
from   solana.rpc.api           import Client
from   solana.rpc.commitment    import Commitment
from   anchorpy.error           import AccountInvalidDiscriminator
from   anchorpy.utils.rpc       import get_multiple_accounts
from   anchorpy.borsh_extension import BorshPubkey

# =============================================================================
#
#POOL_INFO_LAYOUT = borsh.CStruct(
#    "instruction"   / borsh.U8,
#    "simulate_type" / borsh.U8,
#)

# =============================================================================
# Configuration when initializing AMM liquidity pool
@dataclass
class RaydiumLiquidityPoolConfigV4:
    layout: typing.ClassVar = borsh.CStruct(
        "instruction" / borsh.U8,
        "nonce"       / borsh.U8,
        "openTime"    / borsh.U64,
        "pcAmount"    / borsh.U64,
        "coinAmount"  / borsh.U64,
    )
    instruction: int
    nonce:       int
    openTime:    int
    pcAmount:    int
    coinAmount:  int

    # ========================================
    #
    @classmethod
    def decode(cls, data: bytes) -> "RaydiumLiquidityPoolConfigV4":
        dec = RaydiumLiquidityPoolConfigV4.layout.parse(data)
        return cls(instruction = dec.instruction,
                   nonce       = dec.nonce,
                   openTime    = dec.openTime,
                   pcAmount    = dec.pcAmount,
                   coinAmount  = dec.coinAmount)

# =============================================================================
#
