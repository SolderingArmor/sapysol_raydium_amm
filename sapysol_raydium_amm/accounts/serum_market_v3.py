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
# module: Raydium Serum Market Layout
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
from   sapysol                  import MakePubkey, FetchAccount, FetchAccounts

# =============================================================================
#
class SerumMarketV3_JSON(TypedDict):
    padding1:               List[int]
    padding2:               List[int] # accountFlagsLayout('accountFlags'),
    ownAddress:             Pubkey
    vaultSignerNonce:       int
    baseMint:               Pubkey
    quoteMint:              Pubkey
    baseVault:              Pubkey
    baseDepositsTotal:      int
    baseFeesAccrued:        int
    quoteVault:             Pubkey
    quoteDepositsTotal:     int
    quoteFeesAccrued:       int
    quoteDustThreshold:     int
    requestQueue:           Pubkey
    eventQueue:             Pubkey
    bids:                   Pubkey
    asks:                   Pubkey
    baseLotSize:            int
    quoteLotSize:           int
    feeRateBps:             int
    referrerRebatesAccrued: int
    padding3:               List[int]


# =============================================================================
#
@dataclass
class SerumMarketV3:
    layout: ClassVar = borsh.CStruct(
        "padding1"               / borsh.U8[5],
        "padding2"               / borsh.U8[8], # accountFlagsLayout('accountFlags'),
        "ownAddress"             / BorshPubkey,
        "vaultSignerNonce"       / borsh.U64,
        "baseMint"               / BorshPubkey,
        "quoteMint"              / BorshPubkey,
        "baseVault"              / BorshPubkey,
        "baseDepositsTotal"      / borsh.U64,
        "baseFeesAccrued"        / borsh.U64,
        "quoteVault"             / BorshPubkey,
        "quoteDepositsTotal"     / borsh.U64,
        "quoteFeesAccrued"       / borsh.U64,
        "quoteDustThreshold"     / borsh.U64,
        "requestQueue"           / BorshPubkey,
        "eventQueue"             / BorshPubkey,
        "bids"                   / BorshPubkey,
        "asks"                   / BorshPubkey,
        "baseLotSize"            / borsh.U64,
        "quoteLotSize"           / borsh.U64,
        "feeRateBps"             / borsh.U64,
        "referrerRebatesAccrued" / borsh.U64,
        "padding3"               / borsh.U8[7],
    )
    padding1:               List[int]
    padding2:               List[int] # accountFlagsLayout('accountFlags'),
    ownAddress:             Pubkey
    vaultSignerNonce:       int
    baseMint:               Pubkey
    quoteMint:              Pubkey
    baseVault:              Pubkey
    baseDepositsTotal:      int
    baseFeesAccrued:        int
    quoteVault:             Pubkey
    quoteDepositsTotal:     int
    quoteFeesAccrued:       int
    quoteDustThreshold:     int
    requestQueue:           Pubkey
    eventQueue:             Pubkey
    bids:                   Pubkey
    asks:                   Pubkey
    baseLotSize:            int
    quoteLotSize:           int
    feeRateBps:             int
    referrerRebatesAccrued: int
    padding3:               List[int]

    # ========================================
    #
    @classmethod
    def fetch(cls,
              conn:       Client,
              address:    Pubkey,
              commitment: Optional[Commitment] = None) -> Optional["SerumMarketV3"]:

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
                       commitment: Optional[Commitment] = None) -> List[Optional["SerumMarketV3"]]:

        entries = FetchAccounts(connection   = conn, 
                                pubkeys      = addresses,
                                commitment   = commitment)
        return [ SerumMarketV3.decode(entry.data) if entry else None for entry in entries ]

    # ========================================
    #
    @classmethod
    def decode(cls, data: bytes) -> "SerumMarketV3":
        dec = SerumMarketV3.layout.parse(data)
        return cls(padding1               = dec.padding1,
                   padding2               = dec.padding2,
                   ownAddress             = dec.ownAddress,
                   vaultSignerNonce       = dec.vaultSignerNonce,
                   baseMint               = dec.baseMint,
                   quoteMint              = dec.quoteMint,
                   baseVault              = dec.baseVault,
                   baseDepositsTotal      = dec.baseDepositsTotal,
                   baseFeesAccrued        = dec.baseFeesAccrued,
                   quoteVault             = dec.quoteVault,
                   quoteDepositsTotal     = dec.quoteDepositsTotal,
                   quoteFeesAccrued       = dec.quoteFeesAccrued,
                   quoteDustThreshold     = dec.quoteDustThreshold,
                   requestQueue           = dec.requestQueue,
                   eventQueue             = dec.eventQueue,
                   bids                   = dec.bids,
                   asks                   = dec.asks,
                   baseLotSize            = dec.baseLotSize,
                   quoteLotSize           = dec.quoteLotSize,
                   feeRateBps             = dec.feeRateBps,
                   referrerRebatesAccrued = dec.referrerRebatesAccrued,
                   padding3               = dec.padding3)

    # ========================================
    #
    def to_json(self) -> SerumMarketV3_JSON:
        return {
            "padding1":               self.padding1,
            "padding2":               self.padding2,
            "ownAddress":         str(self.ownAddress),
            "vaultSignerNonce":       self.vaultSignerNonce,
            "baseMint":           str(self.baseMint),
            "quoteMint":          str(self.quoteMint),
            "baseVault":          str(self.baseVault),
            "baseDepositsTotal":      self.baseDepositsTotal,
            "baseFeesAccrued":        self.baseFeesAccrued,
            "quoteVault":         str(self.quoteVault),
            "quoteDepositsTotal":     self.quoteDepositsTotal,
            "quoteFeesAccrued":       self.quoteFeesAccrued,
            "quoteDustThreshold":     self.quoteDustThreshold,
            "requestQueue":       str(self.requestQueue),
            "eventQueue":         str(self.eventQueue),
            "bids":               str(self.bids),
            "asks":               str(self.asks),
            "baseLotSize":            self.baseLotSize,
            "quoteLotSize":           self.quoteLotSize,
            "feeRateBps":             self.feeRateBps,
            "referrerRebatesAccrued": self.referrerRebatesAccrued,
            "padding3":               self.padding3,
        }

    # ========================================
    #
    @classmethod
    def from_json(cls, obj: SerumMarketV3_JSON) -> "SerumMarketV3":
        return cls(padding1           =            obj["padding1"],
                   padding2           =            obj["padding2"],
                   ownAddress         = MakePubkey(obj["ownAddress"]),
                   vaultSignerNonce   =            obj["vaultSignerNonce"],
                   baseMint           = MakePubkey(obj["baseMint"]),
                   quoteMint          = MakePubkey(obj["quoteMint"]),
                   baseVault          = MakePubkey(obj["baseVault"]),
                   baseDepositsTotal  =            obj["baseDepositsTotal"],
                   baseFeesAccrued    =            obj["baseFeesAccrued"],
                   quoteVault         = MakePubkey(obj["quoteVault"]),
                   quoteDepositsTotal =            obj["quoteDepositsTotal"],
                   quoteFeesAccrued   =            obj["quoteFeesAccrued"],
                   quoteDustThreshold =            obj["quoteDustThreshold"],
                   requestQueue       = MakePubkey(obj["requestQueue"]),
                   eventQueue         = MakePubkey(obj["eventQueue"]),
                   bids               = MakePubkey(obj["bids"]),
                   asks               = MakePubkey(obj["asks"]),
                   baseLotSize        =            obj["baseLotSize"],
                   quoteLotSize       =            obj["quoteLotSize"],
                   feeRateBps         =            obj["feeRateBps"],
                   referrerRebatesAccrued =        obj["referrerRebatesAccrued"],
                   padding3           =            obj["padding3"])

# =============================================================================
# 
