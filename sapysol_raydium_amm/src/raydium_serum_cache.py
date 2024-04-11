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
# module: raydium serum cache
#
# =============================================================================
# 
from   solana.rpc.api           import Client, Pubkey, Keypair
from   typing                   import List, Any, TypedDict, Union, Optional
from   sapysol                  import *
from ..accounts.serum_market_v3 import *
import logging
import json
import os

# =============================================================================
# 
class RaydiumSerumCache:
    # ========================================
    #
    @staticmethod
    def __RaydiumSerumCachePath() -> str:
        path = os.path.join(os.getenv("HOME"), ".sapysol", "raydium")
        EnsurePathExists(path)
        return path

    @staticmethod
    def __RaydiumSerumFilename(marketAddress: Union[str, Pubkey]) -> str:
        return os.path.join(RaydiumSerumCache.__RaydiumSerumCachePath(), f"{MakePubkey(marketAddress)}.json")

    # ========================================
    #
    @staticmethod
    def __LoadSerumFromFile(marketAddress: Union[str, Pubkey]) -> SerumMarketV3:
        try:
            serumCachePath: str = RaydiumSerumCache.__RaydiumSerumCachePath()
            serumInfoFile:  str = RaydiumSerumCache.__RaydiumSerumFilename(marketAddress=marketAddress)
            logging.debug(f"Loading Raydium AMM Info from file: {serumInfoFile}")
            if not os.path.isfile(serumInfoFile):
                return None
            with open(serumInfoFile) as f:
                serumInfoJson = json.load(f)
                serumEntry = SerumMarketV3.from_json(serumInfoJson)
                return serumEntry
        except:
            return None

    # ========================================
    #
    @staticmethod
    def __LoadSerumFromBlockchain(connection: Client, marketAddress: Union[str, Pubkey]) -> SerumMarketV3:
        serumCachePath: str = RaydiumSerumCache.__RaydiumSerumCachePath()
        serumInfoFile:  str = RaydiumSerumCache.__RaydiumSerumFilename(marketAddress=marketAddress)

        logging.debug(f"Loading Raydium AMM Info from Solana Node for AMM ID: {str(marketAddress)}")
        serumEntry = SerumMarketV3.fetch(conn=connection, address=marketAddress)
        
        with open(serumInfoFile, "w") as f:
            json.dump(serumEntry.to_json(), f)
        return serumEntry

    # ========================================
    #
    @staticmethod
    def UpdateRaydiumSerumCache(connection: Client, marketAddress: Union[str, Pubkey]) -> SerumMarketV3:
        return RaydiumSerumCache.__LoadSerumFromBlockchain(connection=connection, marketAddress=marketAddress)

    @staticmethod
    def GetRaydiumSerum(connection: Client, marketAddress: Union[str, Pubkey]) -> SerumMarketV3:
        serumInfo = RaydiumSerumCache.__LoadSerumFromFile(marketAddress=marketAddress)
        return serumInfo if serumInfo else RaydiumSerumCache.__LoadSerumFromBlockchain(connection=connection, marketAddress=marketAddress)

# =============================================================================
# 
