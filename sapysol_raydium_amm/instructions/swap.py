# ================================================================================
#
from  __future__ import annotations
from    typing                 import Optional, TypedDict, List
from    solders.instruction    import Instruction, AccountMeta
from    spl.token.constants    import ASSOCIATED_TOKEN_PROGRAM_ID, TOKEN_PROGRAM_ID
from    sapysol                import SapysolPubkey, MakePubkey, GetAta
import  borsh_construct        as borsh
from  ..src.constants          import RAYDIUM_SERUM_PROGAM_ID, RAYDIUM_LIQUIDITY_POOL_V4
from  ..src.raydium_swap_cache import RaydiumSwapCacheEntry

# ================================================================================
#
class SwapArgs(TypedDict):
    amount_in:      int
    min_amount_out: int = 0

# ================================================================================
#
layout = borsh.CStruct(
    "amount_in"      / borsh.U64,
    "min_amount_out" / borsh.U64,
)

# ================================================================================
#
def Swap(args:               SwapArgs,
         swapCache:          RaydiumSwapCacheEntry,
         walletAddress:      SapysolPubkey,
         tokenAtaFrom:       SapysolPubkey,
         tokenAtaTo:         SapysolPubkey,
         tokenProgramID:     SapysolPubkey = TOKEN_PROGRAM_ID,
         remaining_accounts: Optional[List[AccountMeta]] = None) -> Instruction:

    keys: list[AccountMeta] = [
        AccountMeta(pubkey=MakePubkey(tokenProgramID),   is_signer=False, is_writable=False),
        AccountMeta(pubkey=swapCache.amm_id,             is_signer=False, is_writable=True ),
        AccountMeta(pubkey=swapCache.authority,          is_signer=False, is_writable=False),
        AccountMeta(pubkey=swapCache.open_orders,        is_signer=False, is_writable=True ),
        AccountMeta(pubkey=swapCache.target_orders,      is_signer=False, is_writable=True ),
        AccountMeta(pubkey=swapCache.base_vault,         is_signer=False, is_writable=True ),
        AccountMeta(pubkey=swapCache.quote_vault,        is_signer=False, is_writable=True ),
        AccountMeta(pubkey=RAYDIUM_SERUM_PROGAM_ID,      is_signer=False, is_writable=False),
        AccountMeta(pubkey=swapCache.market_id,          is_signer=False, is_writable=True ),
        AccountMeta(pubkey=swapCache.bids,               is_signer=False, is_writable=True ),
        AccountMeta(pubkey=swapCache.asks,               is_signer=False, is_writable=True ),
        AccountMeta(pubkey=swapCache.event_queue,        is_signer=False, is_writable=True ),
        AccountMeta(pubkey=swapCache.market_base_vault,  is_signer=False, is_writable=True ),
        AccountMeta(pubkey=swapCache.market_quote_vault, is_signer=False, is_writable=True ),
        AccountMeta(pubkey=swapCache.market_authority,   is_signer=False, is_writable=False),
        AccountMeta(pubkey=MakePubkey(tokenAtaFrom),     is_signer=False, is_writable=True ), # UserSourceTokenAccount
        AccountMeta(pubkey=MakePubkey(tokenAtaTo),       is_signer=False, is_writable=True ), # UserDestTokenAccount
        AccountMeta(pubkey=MakePubkey(walletAddress),    is_signer=True,  is_writable=False)  # UserOwner
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x09"
    encoded_args = layout.build({
        "amount_in":      args["amount_in"],
        "min_amount_out": args["min_amount_out"],
    })
    data = identifier + encoded_args
    return Instruction(RAYDIUM_LIQUIDITY_POOL_V4, data, keys)

# ================================================================================
#
