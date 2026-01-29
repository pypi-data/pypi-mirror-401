from mm_apt.balance import get_balance
from mm_apt.coin import APTOS_COIN_TYPE, USDT_METADATA


async def test_get_balance(mainnet_rpc_url, okx_address):
    res = await get_balance(mainnet_rpc_url, okx_address, APTOS_COIN_TYPE)
    assert res.unwrap() > 1000


async def test_get_balance_usdt(mainnet_rpc_url, okx_address):
    res = await get_balance(mainnet_rpc_url, okx_address, USDT_METADATA)
    assert res.unwrap() > 0
