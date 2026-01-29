from mm_http import http_request
from mm_result import Result


async def get_balance(node: str, account: str, coin_type: str, timeout: float = 5, proxy: str | None = None) -> Result[int]:
    url = f"{node}/view"

    if "::" in coin_type:
        # Coin type (e.g., 0x1::aptos_coin::AptosCoin)
        body = {
            "function": "0x1::coin::balance",
            "type_arguments": [coin_type],
            "arguments": [account],
        }
    else:
        # Fungible Asset metadata address
        body = {
            "function": "0x1::primary_fungible_store::balance",
            "type_arguments": ["0x1::fungible_asset::Metadata"],
            "arguments": [account, coin_type],
        }

    res = await http_request(url, method="POST", json=body, proxy=proxy, timeout=timeout)
    try:
        json_res = res.parse_json()
        if isinstance(json_res, list) and len(json_res) > 0:
            return res.to_result_ok(int(json_res[0]))
        if isinstance(json_res, dict) and json_res.get("error_code") == "resource_not_found":
            return res.to_result_ok(0)
        return res.to_result_err(f"Unexpected response format: {json_res}")
    except Exception as e:
        return res.to_result_err(e)
