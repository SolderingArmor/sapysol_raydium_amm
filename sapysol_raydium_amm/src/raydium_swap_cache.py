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
# module: raydium swap cache
#
# =============================================================================
# 
from   solana.rpc.api      import Client, Pubkey, Keypair
from   sapysol             import *
from   sapysol.token_cache import *
from  .raydium_amm_cache   import *
from  .raydium_serum_cache import *
from   typing              import List, Any, TypedDict, Union, NamedTuple, Optional, ClassVar
from  .constants           import RAYDIUM_LIQUIDITY_POOL_V4, RAYDIUM_AUTHORITY_V4, RAYDIUM_SERUM_PROGAM_ID
from  .derive              import *
from   dataclasses         import dataclass
import logging
import os

# =============================================================================
# 
SAPYSOL_RAYDIUM_VERSION: int = 1

# =============================================================================
# 
class RaydiumSwapCacheEntryJSON(TypedDict):
    SAPYSOL_RAYDIUM_VERSION: int #
    amm_id:                  str #
    authority:               str #
    base_mint:               str #
    base_decimals:           int #
    quote_mint:              str #
    quote_decimals:          int #
    lp_mint:                 str #
    open_orders:             str #
    target_orders:           str #
    base_vault:              str #
    quote_vault:             str #
    market_id:               str #
    market_base_vault:       str #
    market_quote_vault:      str #
    market_authority:        str #
    bids:                    str #
    asks:                    str #
    event_queue:             str #

# =============================================================================
# 
@dataclass
class RaydiumSwapCacheEntry:
    SAPYSOL_RAYDIUM_VERSION: int    #
    amm_id:                  Pubkey #
    authority:               Pubkey #
    base_mint:               Pubkey #
    base_decimals:           int    #
    quote_mint:              Pubkey #
    quote_decimals:          int    #
    lp_mint:                 Pubkey #
    open_orders:             Pubkey #
    target_orders:           Pubkey #
    base_vault:              Pubkey #
    quote_vault:             Pubkey #
    market_id:               Pubkey #
    market_base_vault:       Pubkey #
    market_quote_vault:      Pubkey #
    market_authority:        Pubkey #
    bids:                    Pubkey #
    asks:                    Pubkey #
    event_queue:             Pubkey #

    # ========================================
    #
    def to_json(self) -> RaydiumSwapCacheEntryJSON:
        return {
            "SAPYSOL_RAYDIUM_VERSION": self.SAPYSOL_RAYDIUM_VERSION, #
            "amm_id":              str(self.amm_id),                 #
            "authority":           str(self.authority),              #
            "base_mint":           str(self.base_mint),              #
            "base_decimals":           self.base_decimals,           #
            "quote_mint":          str(self.quote_mint),             #
            "quote_decimals":          self.quote_decimals,          #
            "lp_mint":             str(self.lp_mint),                #
            "open_orders":         str(self.open_orders),            #
            "target_orders":       str(self.target_orders),          #
            "base_vault":          str(self.base_vault),             #
            "quote_vault":         str(self.quote_vault),            #
            "market_id":           str(self.market_id),              #
            "market_base_vault":   str(self.market_base_vault),      #
            "market_quote_vault":  str(self.market_quote_vault),     #
            "market_authority":    str(self.market_authority),       #
            "bids":                str(self.bids),                   #
            "asks":                str(self.asks),                   #
            "event_queue":         str(self.event_queue),            #
        }

    # ========================================
    #
    @classmethod
    def from_json(cls, obj: RaydiumSwapCacheEntryJSON) -> "RaydiumSwapCacheEntry":
        return cls(SAPYSOL_RAYDIUM_VERSION =       obj["SAPYSOL_RAYDIUM_VERSION"],
                   amm_id             = MakePubkey(obj["amm_id"]),
                   authority          = MakePubkey(obj["authority"]),
                   base_mint          = MakePubkey(obj["base_mint"]),
                   base_decimals      =            obj["base_decimals"],
                   quote_mint         = MakePubkey(obj["quote_mint"]),
                   quote_decimals     =            obj["quote_decimals"],
                   lp_mint            = MakePubkey(obj["lp_mint"]),
                   open_orders        = MakePubkey(obj["open_orders"]),
                   target_orders      = MakePubkey(obj["target_orders"]),
                   base_vault         = MakePubkey(obj["base_vault"]),
                   quote_vault        = MakePubkey(obj["quote_vault"]),
                   market_id          = MakePubkey(obj["market_id"]),
                   market_base_vault  = MakePubkey(obj["market_base_vault"]),
                   market_quote_vault = MakePubkey(obj["market_quote_vault"]),
                   market_authority   = MakePubkey(obj["market_authority"]),
                   bids               = MakePubkey(obj["bids"]),
                   asks               = MakePubkey(obj["asks"]),
                   event_queue        = MakePubkey(obj["event_queue"]))


# =============================================================================
# 
class RaydiumSwapCache:
    # ========================================
    #
    @staticmethod
    def __RaydiumSwapCachePath() -> str:
        path = os.path.join(os.getenv("HOME"), ".sapysol", "raydium_swaps")
        EnsurePathExists(path)
        return path

    @staticmethod
    def __RaydiumSwapFilename(poolAddress: SapysolPubkey) -> str:
        return os.path.join(RaydiumSwapCache.__RaydiumSwapCachePath(), f"{str(MakePubkey(poolAddress))}.json")

    # ========================================
    #
    @staticmethod
    def __LoadSwapFromFile(poolAddress: SapysolPubkey) -> RaydiumSwapCacheEntry:
        try:
            swapCachePath: str = RaydiumSwapCache.__RaydiumSwapCachePath()
            swapInfoFile:  str = RaydiumSwapCache.__RaydiumSwapFilename(poolAddress=poolAddress)
            logging.debug(f"Loading Raydium Swap Info from file: {swapInfoFile}")
            if not os.path.isfile(swapInfoFile):
                return None
            with open(swapInfoFile) as f:
                swapInfoJson = json.load(f)
                if "SAPYSOL_RAYDIUM_VERSION" not in swapInfoJson:
                    return None
                if swapInfoJson["SAPYSOL_RAYDIUM_VERSION"] < SAPYSOL_RAYDIUM_VERSION:
                    return None
                return RaydiumSwapCacheEntry.from_json(swapInfoJson)
        except:
            return None

    # ========================================
    #
    @staticmethod
    def __LoadSwapFromBlockchain(connection: Client, poolAddress: Union[str, Pubkey]) -> RaydiumSwapCacheEntry:
        ammInfo:   RaydiumLiquidityPoolV4 = RaydiumAmmCache.GetRaydiumAmm    (connection=connection, poolAddress   = poolAddress)
        serumInfo: SerumMarketV3          = RaydiumSerumCache.GetRaydiumSerum(connection=connection, marketAddress = ammInfo.marketId)
        swapCachePath: str = RaydiumSwapCache.__RaydiumSwapCachePath()
        swapInfoFile:  str = RaydiumSwapCache.__RaydiumSwapFilename(poolAddress=poolAddress)

        logging.debug(f"Loading Raydium Swap Info from Solana Node for AMM ID: {str(poolAddress)}")

        poolAuthority   = DeriveLiquidityV4AssociatedAuthority(programID=RAYDIUM_LIQUIDITY_POOL_V4)
        marketAuthority = DeriveAssociatedMarketAuthority(programID=RAYDIUM_SERUM_PROGAM_ID, marketID=serumInfo.ownAddress)[0]

        cacheEntry = RaydiumSwapCacheEntry(SAPYSOL_RAYDIUM_VERSION = SAPYSOL_RAYDIUM_VERSION, #
                                           amm_id                  = poolAddress,             #
                                           authority               = poolAuthority,           #
                                           base_mint               = ammInfo.baseMint,        #
                                           base_decimals           = ammInfo.baseDecimal,     #
                                           quote_mint              = ammInfo.quoteMint,       #
                                           quote_decimals          = ammInfo.quoteDecimal,    #
                                           lp_mint                 = ammInfo.lpMint,          #
                                           open_orders             = ammInfo.openOrders,      #
                                           target_orders           = ammInfo.targetOrders,    #
                                           base_vault              = ammInfo.baseVault,       #
                                           quote_vault             = ammInfo.quoteVault,      #
                                           market_id               = ammInfo.marketId,        #
                                           market_base_vault       = serumInfo.baseVault,     #
                                           market_quote_vault      = serumInfo.quoteVault,    #
                                           market_authority        = marketAuthority,         #
                                           bids                    = serumInfo.bids,          #
                                           asks                    = serumInfo.asks,          #
                                           event_queue             = serumInfo.eventQueue)    #
        with open(swapInfoFile, "w") as f:
            json.dump(cacheEntry.to_json(), f)
        return cacheEntry

    # ========================================
    #
    @staticmethod
    def __LoadSwapFromMarketAddress(connection: Client, marketAddress: SapysolPubkey) -> RaydiumSwapCacheEntry:
        serumInfo: SerumMarketV3 = RaydiumSerumCache.GetRaydiumSerum(connection=connection, marketAddress=marketAddress)
        associatedID:            Pubkey = DeriveLiquidityV4AssociatedID           (MakePubkey(marketAddress))
        associatedBaseVault:     Pubkey = DeriveLiquidityV4AssociatedBaseVault    (MakePubkey(marketAddress))
        associatedQuoteVault:    Pubkey = DeriveLiquidityV4AssociatedQuoteVault   (MakePubkey(marketAddress))
        associatedLpMint:        Pubkey = DeriveLiquidityV4AssociatedLpMint       (MakePubkey(marketAddress))
        associatedLpVault:       Pubkey = DeriveLiquidityV4AssociatedLpVault      (MakePubkey(marketAddress))
        associatedTargetOrders:  Pubkey = DeriveLiquidityV4AssociatedTargetOrders (MakePubkey(marketAddress))
        associatedWithdrawQueue: Pubkey = DeriveLiquidityV4AssociatedWithdrawQueue(MakePubkey(marketAddress))
        associatedOpenOrders:    Pubkey = DeriveLiquidityV4AssociatedOpenOrders   (MakePubkey(marketAddress))
        associatedConfigId:      Pubkey = DeriveLiquidityV4AssociatedConfigId()

        swapInfoFile:  str = RaydiumSwapCache.__RaydiumSwapFilename(poolAddress=associatedID)
        
        poolAuthority   = DeriveLiquidityV4AssociatedAuthority(programID=RAYDIUM_LIQUIDITY_POOL_V4)
        marketAuthority = DeriveAssociatedMarketAuthority(programID=RAYDIUM_SERUM_PROGAM_ID, marketID=serumInfo.ownAddress)[0]

        baseToken:  TokenCacheEntry = TokenCache.GetToken(connection=connection, tokenMint=serumInfo.baseMint )
        quoteToken: TokenCacheEntry = TokenCache.GetToken(connection=connection, tokenMint=serumInfo.quoteMint)

        cacheEntry = RaydiumSwapCacheEntry(SAPYSOL_RAYDIUM_VERSION = SAPYSOL_RAYDIUM_VERSION, #
                                           amm_id                  = associatedID,            #
                                           authority               = poolAuthority,           #
                                           base_mint               = serumInfo.baseMint,      #
                                           base_decimals           = baseToken.decimals,      #
                                           quote_mint              = serumInfo.quoteMint,     #
                                           quote_decimals          = quoteToken.decimals,     #
                                           lp_mint                 = associatedLpMint,        #
                                           open_orders             = associatedOpenOrders,    #
                                           target_orders           = associatedTargetOrders,  #
                                           base_vault              = associatedBaseVault,     #
                                           quote_vault             = associatedQuoteVault,    #
                                           market_id               = serumInfo.ownAddress,    #
                                           market_base_vault       = serumInfo.baseVault,     #
                                           market_quote_vault      = serumInfo.quoteVault,    #
                                           market_authority        = marketAuthority,         #
                                           bids                    = serumInfo.bids,          #
                                           asks                    = serumInfo.asks,          #
                                           event_queue             = serumInfo.eventQueue)    #
        with open(swapInfoFile, "w") as f:
            json.dump(cacheEntry, f)
        return cacheEntry

    # ========================================
    #
    @staticmethod
    def UpdateSwapCacheFromPoolAddress(connection: Client, poolAddress: SapysolPubkey) -> RaydiumSwapCacheEntry:
        return RaydiumSwapCache.__LoadSwapFromBlockchain(connection=connection, poolAddress=poolAddress)

    @staticmethod
    def UpdateSwapCacheFromMarketAddress(connection: Client, marketAddress: SapysolPubkey) -> RaydiumSwapCacheEntry:
        return RaydiumSwapCache.__LoadSwapFromMarketAddress(connection=connection, marketAddress=marketAddress)

    @staticmethod
    def GetSwapCacheFromPoolAddress(connection: Client, poolAddress: SapysolPubkey) -> RaydiumSwapCacheEntry:
        swapInfo = RaydiumSwapCache.__LoadSwapFromFile(poolAddress=poolAddress)
        return swapInfo if swapInfo else RaydiumSwapCache.UpdateSwapCacheFromPoolAddress(connection=connection, poolAddress=poolAddress)

    @staticmethod
    def GetSwapCacheFromMarketAddress(connection: Client, marketAddress: SapysolPubkey) -> RaydiumSwapCacheEntry:
        associatedID: Pubkey = DeriveLiquidityV4AssociatedID(MakePubkey(marketAddress))
        swapInfo = RaydiumSwapCache.__LoadSwapFromFile(poolAddress=associatedID)
        return swapInfo if swapInfo else RaydiumSwapCache.UpdateSwapCacheFromMarketAddress(connection=connection, marketAddress=marketAddress)

# =============================================================================
# 
