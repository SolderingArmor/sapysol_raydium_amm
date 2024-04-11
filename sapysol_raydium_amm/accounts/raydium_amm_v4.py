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
# module: Raydium AMM Layout V4
#
# =============================================================================
# 
import borsh_construct as borsh
from   dataclasses              import dataclass
from   solders.pubkey           import Pubkey
from   solana.rpc.api           import Client
from   solana.rpc.commitment    import Commitment
from   anchorpy.error           import AccountInvalidDiscriminator
from   anchorpy.utils.rpc       import get_multiple_accounts
from   anchorpy.borsh_extension import BorshPubkey
from   typing                   import List, Any, TypedDict, Union, Optional, ClassVar
from   sapysol                  import FetchAccount, FetchAccounts

# =============================================================================
#

class RaydiumLiquidityPoolV4_JSON(TypedDict):
    status:                 int
    nonce:                  int
    maxOrder:               int
    depth:                  int
    baseDecimal:            int
    quoteDecimal:           int
    state:                  int
    resetFlag:              int
    minSize:                int
    volMaxCutRatio:         int
    amountWaveRatio:        int
    baseLotSize:            int
    quoteLotSize:           int
    minPriceMultiplier:     int
    maxPriceMultiplier:     int
    systemDecimalValue:     int
    minSeparateNumerator:   int
    minSeparateDenominator: int
    tradeFeeNumerator:      int
    tradeFeeDenominator:    int
    pnlNumerator:           int
    pnlDenominator:         int
    swapFeeNumerator:       int
    swapFeeDenominator:     int
    baseNeedTakePnl:        int
    quoteNeedTakePnl:       int
    quoteTotalPnl:          int
    baseTotalPnl:           int
    poolOpenTime:           int
    punishPcAmount:         int
    punishCoinAmount:       int
    orderbookToInitTime:    int
    #
    swapBaseInAmount:       int
    swapQuoteOutAmount:     int
    swapBase2QuoteFee:      int
    swapQuoteInAmount:      int
    swapBaseOutAmount:      int
    swapQuote2BaseFee:      int
    #
    baseVault:              Pubkey
    quoteVault:             Pubkey
    #
    baseMint:               Pubkey
    quoteMint:              Pubkey
    lpMint:                 Pubkey
    #
    openOrders:             Pubkey
    marketId:               Pubkey
    marketProgramId:        Pubkey
    targetOrders:           Pubkey
    withdrawQueue:          Pubkey
    lpVault:                Pubkey
    owner:                  Pubkey
    #
    lpReserve:              int
    padding:                list[int]

# =============================================================================
#
@dataclass
class RaydiumLiquidityPoolV4:
    layout: ClassVar = borsh.CStruct(
        "status"                 / borsh.U64,
        "nonce"                  / borsh.U64,
        "maxOrder"               / borsh.U64,
        "depth"                  / borsh.U64,
        "baseDecimal"            / borsh.U64,
        "quoteDecimal"           / borsh.U64,
        "state"                  / borsh.U64,
        "resetFlag"              / borsh.U64,
        "minSize"                / borsh.U64,
        "volMaxCutRatio"         / borsh.U64,
        "amountWaveRatio"        / borsh.U64,
        "baseLotSize"            / borsh.U64,
        "quoteLotSize"           / borsh.U64,
        "minPriceMultiplier"     / borsh.U64,
        "maxPriceMultiplier"     / borsh.U64,
        "systemDecimalValue"     / borsh.U64,
        "minSeparateNumerator"   / borsh.U64,
        "minSeparateDenominator" / borsh.U64,
        "tradeFeeNumerator"      / borsh.U64,
        "tradeFeeDenominator"    / borsh.U64,
        "pnlNumerator"           / borsh.U64,
        "pnlDenominator"         / borsh.U64,
        "swapFeeNumerator"       / borsh.U64,
        "swapFeeDenominator"     / borsh.U64,
        "baseNeedTakePnl"        / borsh.U64,
        "quoteNeedTakePnl"       / borsh.U64,
        "quoteTotalPnl"          / borsh.U64,
        "baseTotalPnl"           / borsh.U64,
        "poolOpenTime"           / borsh.U64,
        "punishPcAmount"         / borsh.U64,
        "punishCoinAmount"       / borsh.U64,
        "orderbookToInitTime"    / borsh.U64,
        # u128('poolTotalDepositPc'),
        # u128('poolTotalDepositCoin'),
        "swapBaseInAmount"       / borsh.U128,
        "swapQuoteOutAmount"     / borsh.U128,
        "swapBase2QuoteFee"      / borsh.U64,
        "swapQuoteInAmount"      / borsh.U128,
        "swapBaseOutAmount"      / borsh.U128,
        "swapQuote2BaseFee"      / borsh.U64,
        # amm vault
        "baseVault"              / BorshPubkey,
        "quoteVault"             / BorshPubkey,
        # mint
        "baseMint"               / BorshPubkey,
        "quoteMint"              / BorshPubkey,
        "lpMint"                 / BorshPubkey,
        # market
        "openOrders"             / BorshPubkey,
        "marketId"               / BorshPubkey,
        "marketProgramId"        / BorshPubkey,
        "targetOrders"           / BorshPubkey,
        "withdrawQueue"          / BorshPubkey,
        "lpVault"                / BorshPubkey,
        "owner"                  / BorshPubkey,
        # true circulating supply without lock up
        "lpReserve"              / borsh.U64,
        "padding"                / borsh.U64[3],
    )
    status:                 int
    nonce:                  int
    maxOrder:               int
    depth:                  int
    baseDecimal:            int
    quoteDecimal:           int
    state:                  int
    resetFlag:              int
    minSize:                int
    volMaxCutRatio:         int
    amountWaveRatio:        int
    baseLotSize:            int
    quoteLotSize:           int
    minPriceMultiplier:     int
    maxPriceMultiplier:     int
    systemDecimalValue:     int
    minSeparateNumerator:   int
    minSeparateDenominator: int
    tradeFeeNumerator:      int
    tradeFeeDenominator:    int
    pnlNumerator:           int
    pnlDenominator:         int
    swapFeeNumerator:       int
    swapFeeDenominator:     int
    baseNeedTakePnl:        int
    quoteNeedTakePnl:       int
    quoteTotalPnl:          int
    baseTotalPnl:           int
    poolOpenTime:           int
    punishPcAmount:         int
    punishCoinAmount:       int
    orderbookToInitTime:    int
    #
    swapBaseInAmount:       int
    swapQuoteOutAmount:     int
    swapBase2QuoteFee:      int
    swapQuoteInAmount:      int
    swapBaseOutAmount:      int
    swapQuote2BaseFee:      int
    #
    baseVault:              Pubkey
    quoteVault:             Pubkey
    #
    baseMint:               Pubkey
    quoteMint:              Pubkey
    lpMint:                 Pubkey
    #
    openOrders:             Pubkey
    marketId:               Pubkey
    marketProgramId:        Pubkey
    targetOrders:           Pubkey
    withdrawQueue:          Pubkey
    lpVault:                Pubkey
    owner:                  Pubkey
    #
    lpReserve:              int
    padding:                list[int]

    # ========================================
    #
    @classmethod
    def fetch(cls,
              conn:       Client,
              address:    Pubkey,
              commitment: Optional[Commitment] = None) -> Optional["RaydiumLiquidityPoolV4"]:

        resp = FetchAccount(connection    = conn, 
                            pubkey        = address,
                            commitment    = commitment)
        return None if resp is None else cls.decode(resp.data)

    # ========================================
    #
    @classmethod
    def fetch_multiple(cls,
                       conn:       Client,
                       addresses:  list[Pubkey],
                       commitment: Optional[Commitment] = None) -> List[Optional["RaydiumLiquidityPoolV4"]]:

        infos = get_multiple_accounts(conn, addresses, commitment=commitment)
        res: List[Optional["RaydiumLiquidityPoolV4"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            res.append(cls.decode(info.account.data))
        return res

    # ========================================
    #
    @classmethod
    def decode(cls, data: bytes) -> "RaydiumLiquidityPoolV4":
        dec = RaydiumLiquidityPoolV4.layout.parse(data)
        return cls(
            status                 = dec.status,
            nonce                  = dec.nonce,
            maxOrder               = dec.maxOrder,
            depth                  = dec.depth,
            baseDecimal            = dec.baseDecimal,
            quoteDecimal           = dec.quoteDecimal,
            state                  = dec.state,
            resetFlag              = dec.resetFlag,
            minSize                = dec.minSize,
            volMaxCutRatio         = dec.volMaxCutRatio,
            amountWaveRatio        = dec.amountWaveRatio,
            baseLotSize            = dec.baseLotSize,
            quoteLotSize           = dec.quoteLotSize,
            minPriceMultiplier     = dec.minPriceMultiplier,
            maxPriceMultiplier     = dec.maxPriceMultiplier,
            systemDecimalValue     = dec.systemDecimalValue,
            minSeparateNumerator   = dec.minSeparateNumerator,
            minSeparateDenominator = dec.minSeparateDenominator,
            tradeFeeNumerator      = dec.tradeFeeNumerator,
            tradeFeeDenominator    = dec.tradeFeeDenominator,
            pnlNumerator           = dec.pnlNumerator,
            pnlDenominator         = dec.pnlDenominator,
            swapFeeNumerator       = dec.swapFeeNumerator,
            swapFeeDenominator     = dec.swapFeeDenominator,
            baseNeedTakePnl        = dec.baseNeedTakePnl,
            quoteNeedTakePnl       = dec.quoteNeedTakePnl,
            quoteTotalPnl          = dec.quoteTotalPnl,
            baseTotalPnl           = dec.baseTotalPnl,
            poolOpenTime           = dec.poolOpenTime,
            punishPcAmount         = dec.punishPcAmount,
            punishCoinAmount       = dec.punishCoinAmount,
            orderbookToInitTime    = dec.orderbookToInitTime,
            #
            swapBaseInAmount       = dec.swapBaseInAmount,
            swapQuoteOutAmount     = dec.swapQuoteOutAmount,
            swapBase2QuoteFee      = dec.swapBase2QuoteFee,
            swapQuoteInAmount      = dec.swapQuoteInAmount,
            swapBaseOutAmount      = dec.swapBaseOutAmount,
            swapQuote2BaseFee      = dec.swapQuote2BaseFee,
            #
            baseVault              = dec.baseVault,
            quoteVault             = dec.quoteVault,
            #
            baseMint               = dec.baseMint,
            quoteMint              = dec.quoteMint,
            lpMint                 = dec.lpMint,
            #
            openOrders             = dec.openOrders,
            marketId               = dec.marketId,
            marketProgramId        = dec.marketProgramId,
            targetOrders           = dec.targetOrders,
            withdrawQueue          = dec.withdrawQueue,
            lpVault                = dec.lpVault,
            owner                  = dec.owner,
            #
            lpReserve              = dec.lpReserve,
            padding                = dec.padding
        )

    # ========================================
    #
    def to_json(self) -> RaydiumLiquidityPoolV4_JSON:
        return {
            "status" :                 self.status,
            "nonce" :                  self.nonce,
            "maxOrder" :               self.maxOrder,
            "depth" :                  self.depth,
            "baseDecimal" :            self.baseDecimal,
            "quoteDecimal" :           self.quoteDecimal,
            "state" :                  self.state,
            "resetFlag" :              self.resetFlag,
            "minSize" :                self.minSize,
            "volMaxCutRatio" :         self.volMaxCutRatio,
            "amountWaveRatio" :        self.amountWaveRatio,
            "baseLotSize" :            self.baseLotSize,
            "quoteLotSize" :           self.quoteLotSize,
            "minPriceMultiplier" :     self.minPriceMultiplier,
            "maxPriceMultiplier" :     self.maxPriceMultiplier,
            "systemDecimalValue" :     self.systemDecimalValue,
            "minSeparateNumerator" :   self.minSeparateNumerator,
            "minSeparateDenominator" : self.minSeparateDenominator,
            "tradeFeeNumerator" :      self.tradeFeeNumerator,
            "tradeFeeDenominator" :    self.tradeFeeDenominator,
            "pnlNumerator" :           self.pnlNumerator,
            "pnlDenominator" :         self.pnlDenominator,
            "swapFeeNumerator" :       self.swapFeeNumerator,
            "swapFeeDenominator" :     self.swapFeeDenominator,
            "baseNeedTakePnl" :        self.baseNeedTakePnl,
            "quoteNeedTakePnl" :       self.quoteNeedTakePnl,
            "quoteTotalPnl" :          self.quoteTotalPnl,
            "baseTotalPnl" :           self.baseTotalPnl,
            "poolOpenTime" :           self.poolOpenTime,
            "punishPcAmount" :         self.punishPcAmount,
            "punishCoinAmount" :       self.punishCoinAmount,
            "orderbookToInitTime" :    self.orderbookToInitTime,
            #
            "swapBaseInAmount" :       self.swapBaseInAmount,
            "swapQuoteOutAmount" :     self.swapQuoteOutAmount,
            "swapBase2QuoteFee" :      self.swapBase2QuoteFee,
            "swapQuoteInAmount" :      self.swapQuoteInAmount,
            "swapBaseOutAmount" :      self.swapBaseOutAmount,
            "swapQuote2BaseFee" :      self.swapQuote2BaseFee,
            #
            "baseVault" :              str(self.baseVault),
            "quoteVault" :             str(self.quoteVault),
            #
            "baseMint" :               str(self.baseMint),
            "quoteMint" :              str(self.quoteMint),
            "lpMint" :                 str(self.lpMint),
            #
            "openOrders" :             str(self.openOrders),
            "marketId" :               str(self.marketId),
            "marketProgramId" :        str(self.marketProgramId),
            "targetOrders" :           str(self.targetOrders),
            "withdrawQueue" :          str(self.withdrawQueue),
            "lpVault" :                str(self.lpVault),
            "owner" :                  str(self.owner),
            #
            "lpReserve" :              self.lpReserve,
            "padding" :                self.padding,
        }

    # ========================================
    #
    @classmethod
    def from_json(cls, obj: RaydiumLiquidityPoolV4_JSON) -> "RaydiumLiquidityPoolV4":
        return cls(status                 = obj["status"],
                   nonce                  = obj["nonce"],
                   maxOrder               = obj["maxOrder"],
                   depth                  = obj["depth"],
                   baseDecimal            = obj["baseDecimal"],
                   quoteDecimal           = obj["quoteDecimal"],
                   state                  = obj["state"],
                   resetFlag              = obj["resetFlag"],
                   minSize                = obj["minSize"],
                   volMaxCutRatio         = obj["volMaxCutRatio"],
                   amountWaveRatio        = obj["amountWaveRatio"],
                   baseLotSize            = obj["baseLotSize"],
                   quoteLotSize           = obj["quoteLotSize"],
                   minPriceMultiplier     = obj["minPriceMultiplier"],
                   maxPriceMultiplier     = obj["maxPriceMultiplier"],
                   systemDecimalValue     = obj["systemDecimalValue"],
                   minSeparateNumerator   = obj["minSeparateNumerator"],
                   minSeparateDenominator = obj["minSeparateDenominator"],
                   tradeFeeNumerator      = obj["tradeFeeNumerator"],
                   tradeFeeDenominator    = obj["tradeFeeDenominator"],
                   pnlNumerator           = obj["pnlNumerator"],
                   pnlDenominator         = obj["pnlDenominator"],
                   swapFeeNumerator       = obj["swapFeeNumerator"],
                   swapFeeDenominator     = obj["swapFeeDenominator"],
                   baseNeedTakePnl        = obj["baseNeedTakePnl"],
                   quoteNeedTakePnl       = obj["quoteNeedTakePnl"],
                   quoteTotalPnl          = obj["quoteTotalPnl"],
                   baseTotalPnl           = obj["baseTotalPnl"],
                   poolOpenTime           = obj["poolOpenTime"],
                   punishPcAmount         = obj["punishPcAmount"],
                   punishCoinAmount       = obj["punishCoinAmount"],
                   orderbookToInitTime    = obj["orderbookToInitTime"],
                   #
                   swapBaseInAmount       = obj["swapBaseInAmount"],
                   swapQuoteOutAmount     = obj["swapQuoteOutAmount"],
                   swapBase2QuoteFee      = obj["swapBase2QuoteFee"],
                   swapQuoteInAmount      = obj["swapQuoteInAmount"],
                   swapBaseOutAmount      = obj["swapBaseOutAmount"],
                   swapQuote2BaseFee      = obj["swapQuote2BaseFee"],
                   #
                   baseVault              = Pubkey.from_string(obj["baseVault"]),
                   quoteVault             = Pubkey.from_string(obj["quoteVault"]),
                   #
                   baseMint               = Pubkey.from_string(obj["baseMint"]),
                   quoteMint              = Pubkey.from_string(obj["quoteMint"]),
                   lpMint                 = Pubkey.from_string(obj["lpMint"]),
                   #
                   openOrders             = Pubkey.from_string(obj["openOrders"]),
                   marketId               = Pubkey.from_string(obj["marketId"]),
                   marketProgramId        = Pubkey.from_string(obj["marketProgramId"]),
                   targetOrders           = Pubkey.from_string(obj["targetOrders"]),
                   withdrawQueue          = Pubkey.from_string(obj["withdrawQueue"]),
                   lpVault                = Pubkey.from_string(obj["lpVault"]),
                   owner                  = Pubkey.from_string(obj["owner"]),
                   #
                   lpReserve              = obj["lpReserve"],
                   padding                = obj["padding"])

# =============================================================================
#
