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
# module: Raydium AMM
#
# =============================================================================
# 
from   solana.rpc.api          import Client, Pubkey, Keypair
from   typing                  import List, Any, TypedDict, Union, Optional
from   sapysol                 import *
from   sapysol.token_cache     import TokenCacheEntry, TokenCache
from   solders.instruction     import Instruction
from   spl.token.constants     import WRAPPED_SOL_MINT
from  .src.raydium_swap_cache  import RaydiumSwapCacheEntry, RaydiumSwapCache
from  .instructions.swap       import SwapArgs, Swap
import logging
import json
import os

# =============================================================================
# 
class SapysolRaydiumAMM:
    def __init__(self, connection: Client, swapCache: RaydiumSwapCacheEntry):
        self.CONNECTION: Client                = connection
        self.SWAP_CACHE: RaydiumSwapCacheEntry = swapCache

    # ========================================
    #
    @staticmethod
    def FromPoolAddress(connection: Client, poolAddress: SapysolPubkey) -> "SapysolRaydiumAMM":
        swapCache: RaydiumSwapCacheEntry = RaydiumSwapCache.GetSwapCacheFromPoolAddress(connection=connection, poolAddress=poolAddress)
        return SapysolRaydiumAMM(connection=connection, swapCache=swapCache)

    # ========================================
    #
    @staticmethod
    def FromMarketAddress(connection: Client, marketAddress: SapysolPubkey) -> "SapysolRaydiumAMM":
        swapCache: RaydiumSwapCacheEntry = RaydiumSwapCache.GetSwapCacheFromMarketAddress(connection=connection, marketAddress=marketAddress)
        return SapysolRaydiumAMM(connection=connection, swapCache=swapCache)

    # ========================================
    #
    def UpdateCache(self):
        self.SWAP_CACHE: RaydiumSwapCacheEntry = RaydiumSwapCache.UpdateSwapCacheFromPoolAddress(connection  = self.CONNECTION, 
                                                                                                 poolAddress = self.SWAP_CACHE.amm_id)

    # ========================================
    #
    def GetSwapInstruction(self, 
                           walletAddress:     SapysolPubkey,
                           tokenFrom:         SapysolPubkey, # Sanity
                           tokenTo:           SapysolPubkey, # Sanity
                           amountIn:          Union[int, float],
                           desiredAmountOut:  Optional[Union[int, float]] = None,
                           inLamports:        bool = True,
                           wrapSol:           bool = True,
                           unwrapSol:         bool = True,
                           txComputePrice:    int = 1) -> Optional[List[Instruction]]:

        assert(MakePubkey(tokenFrom) in [self.SWAP_CACHE.base_mint, self.SWAP_CACHE.quote_mint])
        assert(MakePubkey(tokenTo)   in [self.SWAP_CACHE.base_mint, self.SWAP_CACHE.quote_mint])

        cachedTokenFrom: TokenCacheEntry = TokenCache.GetToken(connection=self.CONNECTION, tokenMint=tokenFrom)
        cachedTokenTo:   TokenCacheEntry = TokenCache.GetToken(connection=self.CONNECTION, tokenMint=tokenTo  )

        amountInLamports:           int = amountIn if inLamports else amountIn * (10**cachedTokenFrom.decimals)
        desiredAmountOutInLamports: int = 0 if desiredAmountOut is None       \
                                          else desiredAmountOut if inLamports \
                                                              else desiredAmountOut * (10**cachedTokenTo.decimals)

        amountInLamports           = int(amountInLamports)
        desiredAmountOutInLamports = int(desiredAmountOutInLamports)

        ixSwap = Swap(args           = SwapArgs(amount_in=amountInLamports, min_amount_out=desiredAmountOutInLamports),
                      swapCache      = self.SWAP_CACHE,
                      walletAddress  = walletAddress,
                      tokenAtaFrom   = GetAta(tokenMint=tokenFrom, owner=walletAddress),
                      tokenAtaTo     = GetAta(tokenMint=tokenTo,   owner=walletAddress),
                      tokenProgramID = cachedTokenTo.program_id)

        ixList: List[Instruction] = []
        # 1. Budget
        ixList.append(ComputeBudgetIx())
        ixList.append(ComputePriceIx(txComputePrice))
        # 2. Wrap SOL?
        if tokenFrom == WRAPPED_SOL_MINT:
            if wrapSol:
                ixList += WrapSolInstructions(connection=self.CONNECTION, lamports=amountInLamports, owner=walletAddress)

        # 3. Create ATA of a token TO if needed
        tokenToAtaIx = GetOrCreateAtaIx(connection=self.CONNECTION, tokenMint=tokenTo, owner=walletAddress)
        if tokenToAtaIx.ix:
            ixList.append(tokenToAtaIx.ix)
        # 4. Swap
        ixList.append(ixSwap)
        # 5. Unwrap SOL and close account if needed
        if tokenTo == WRAPPED_SOL_MINT and unwrapSol:
            ixList.append(UnwrapSolInstruction(owner=walletAddress))

        return ixList

# =============================================================================
# 
