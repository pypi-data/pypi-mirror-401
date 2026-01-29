from mm_apt import ans


async def test_address_to_primary_name():
    address = "0xfe2ffdb3a74307f7314a1c8ab3762b6b5869a3c1278cdd5d230249453e15a1db"
    assert (await ans.address_to_primary_name(address)).unwrap() is None

    address = "0xabfabdec0732564bd906fb94e467410a131c6e6040f7bca860458e2026e3b14e"
    assert (await ans.address_to_primary_name(address)).unwrap() is None


async def test_address_to_name():
    address = "0xfe2ffdb3a74307f7314a1c8ab3762b6b5869a3c1278cdd5d230249453e15a1db"
    assert (await ans.address_to_name(address)).unwrap() == "petra"

    address = "0xabfabdec0732564bd906fb94e467410a131c6e6040f7bca860458e2026e3b14e"
    assert (await ans.address_to_name(address)).unwrap() is None
