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
# module: raydium amm cache
#
# =============================================================================
# 
from   solana.rpc.api           import Client, Pubkey, Keypair
from   typing                   import List, Any, TypedDict, Union, Optional
from   sapysol                  import *
from ..accounts.raydium_amm_v4  import *
import logging
import json
import os

# =============================================================================
# 
class RaydiumAmmCache:
    # ========================================
    #
    @staticmethod
    def __RaydiumAmmCachePath() -> str:
        path = os.path.join(os.getenv("HOME"), ".sapysol", "raydium")
        EnsurePathExists(path)
        return path

    @staticmethod
    def __RaydiumAmmFilename(poolAddress: Union[str, Pubkey]) -> str:
        return os.path.join(RaydiumAmmCache.__RaydiumAmmCachePath(), f"{MakePubkey(poolAddress)}.json")

    # ========================================
    #
    @staticmethod
    def __LoadAmmFromFile(poolAddress: Union[str, Pubkey]) -> RaydiumLiquidityPoolV4:
        try:
            ammCachePath: str = RaydiumAmmCache.__RaydiumAmmCachePath()
            ammInfoFile:  str = RaydiumAmmCache.__RaydiumAmmFilename(poolAddress=poolAddress)
            logging.debug(f"Loading Raydium AMM Info from file: {ammInfoFile}")
            if not os.path.isfile(ammInfoFile):
                return None
            with open(ammInfoFile) as f:
                ammInfoJson = json.load(f)
                ammEntry = RaydiumLiquidityPoolV4.from_json(ammInfoJson)
                return ammEntry
        except:
            return None

    # ========================================
    #
    @staticmethod
    def __LoadAmmFromBlockchain(connection: Client, poolAddress: Union[str, Pubkey]) -> RaydiumLiquidityPoolV4:
        ammCachePath: str = RaydiumAmmCache.__RaydiumAmmCachePath()
        ammInfoFile:  str = RaydiumAmmCache.__RaydiumAmmFilename(poolAddress=poolAddress)

        logging.debug(f"Loading Raydium AMM Info from Solana Node for AMM ID: {str(poolAddress)}")
        ammEntry = RaydiumLiquidityPoolV4.fetch(conn=connection, address=poolAddress)
        
        with open(ammInfoFile, "w") as f:
            json.dump(ammEntry.to_json(), f)
        return ammEntry

    # ========================================
    #
    @staticmethod
    def UpdateRaydiumAmmCache(connection: Client, poolAddress: Union[str, Pubkey]) -> RaydiumLiquidityPoolV4:
        return RaydiumAmmCache.__LoadAmmFromBlockchain(connection=connection, poolAddress=poolAddress)

    @staticmethod
    def GetRaydiumAmm(connection: Client, poolAddress: Union[str, Pubkey]) -> RaydiumLiquidityPoolV4:
        ammInfo = RaydiumAmmCache.__LoadAmmFromFile(poolAddress=poolAddress)
        return ammInfo if ammInfo else RaydiumAmmCache.__LoadAmmFromBlockchain(connection=connection, poolAddress=poolAddress)

# =============================================================================
# 
