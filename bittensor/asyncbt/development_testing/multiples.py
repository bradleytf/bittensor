import asyncio
from pprint import PrettyPrinter
import time

import bittensor
from bittensor import subtensor_module
from bittensor.asyncbt.utils import rpc_requests


pp = PrettyPrinter(indent=4).pprint


async def get_delegated(ss58: str, rpc: rpc_requests.RPCRequest):
    encoded = subtensor_module.ss58_to_vec_u8(ss58)
    id_ = "Encoded Get Delegated"
    payload = {
        15: {
            "id": id_,
            "payload": {
                "jsonrpc": "2.0",
                "method": "delegateInfo_getDelegated",
                "params": [encoded],
                "id": 15
            }
        }
    }
    result = await rpc._make_rpc_request(payload, None, None, None)
    return result[id_][0]["result"]


async def root_list(block_hash, rpc: rpc_requests.RPCRequest):
    hotkeys__ = (
        "5GHczYXpzd5xmNwjxWs63hw9DannNBGDp6tG6aPmsqP5WiwM 5CP9yFmNqiafpXDsTrdZvFpGgnGUkmGW2geM4TZPJmWYaVu2 "
        "5CvjMLhb492gaZrJFauY87qMMwJomKuK7dTUaXgdUanLTU9Z 5FLDSzoPejcrQW5CYbXvq7WE5X9NL6SFD4xJqmyjc72xUhHE "
        "5FqBhsQwGNUeJ2RZuCVQxSxRYD7sEbH15ixc5hMgihbAmcu9 5Hddm3iBFD2GLT5ik7LZnT3XJUnRnN8PoeCFgGQgawUVKNm8 "
        "5DvFEV5nBSdoKftxisu5EM63PzPsVTD7zuq6XTnCDcbCy3Rz 5Csui1uEQiKfgcvCf1ZEaEE2AUihzWXnFES3VUNnPtZ8rzBX "
        "5GuNeKJGihxrnNokQdviGkeCM3qTGX2vbVPaQ4Ktki9uEqso 5HJua76UDcLwDci6kf8hDHcQBnPM7u3cPfjitBBaJkTVmEYh "
        "5DyfyYuESbmzea9jTiy9iMuKE6RvQjowKRxeZ6UnBUiYoC5y 5Dk2y7wgtnrkN5C7BQYTmrTNoU3vhko5d2wtc8w6bVsmoAtF "
        "5C86aJ2uQawR6P6veaJQXNK9HaWh6NMbUhTiLs65kq4ZW3NH 5ExZhGZerURnunK2g5rjAaCNvBXYTCJguf2SSzWVZQZfr21T "
        "5G9WcjZvv2n6qLdpsMqEDHwvtondiiZJnDmbrGrAyC7B573o 5EhEZN6soubtKJm8RN7ANx9FGZ2JezxBUFxr45cdsHtDp3Uk "
        "5D1rWnzozRX68ZqKTPXZAFWTJ8hHpox283yWFmsdNjxhRCdB 5ECDEtiHDP7tXeG3L7PViHsjSUPCsijKEokrFWhdXuATDjH1 "
        "5HTZipxVCMqzhLt9QKi2Nxj3Fd6TCSnzTjBKR3vtiuTkuq1B 5CMPL2Fq5tNVM1isoiU6kdaUYg9fi5Cfpstwp2rzY5G9EYM8 "
        "5Fjp4r8cvWexkWUVb756LkopTVjmzXHBT4unpDN6SzwmQq8E 5HZ5FuwCarNA1CQqCYBcWMSNdUkcjKoCTDknJWz5ZRwh3ZM3 "
        "5HjSBYq1yEt7BNycCMuvdhSB7guwgZXNmauscZVAzBQAro8E 5DHeZzocsGn2qgqENUEa2TT6dT23cwJ6sCXb9Bngrtr9etLQ "
        "5FFE2bL4hJgGNJzfm7rCAXiVscZbEF13m9DxCewstp3XPK61 5FYkcKakNcckoA37uDrKVuc6pvzFXWThQLkBbM7yxTkP3AtN "
        "5HBMRwHL76GpLXA4VesQPicWL7rPS4CtMWhm5oa4D4kwQgzC 5GQfE6zGrjU2g88ow7cAGdDCE6fXQMgFkeX2ejtHv8C4YWuP "
        "5FBfMAnR3PkvvvxBbPfC9YbdW25jsyhyB7p1BZtckCuDjBQn 5CqgbUYinK8k6pgSoDRLggxJMgTv3cBNiyRRYTkpCt3SKQ5Y "
        "5GEfySfTspQocWmXra4gJgVWy71tk8WySbXpU1vAPP2evaUF 5GTpXGKbcoA4Wor2LvZpTU913EDV2AbjMXPLGKCkNukjPvwY "
        "5EJEfB4wasHRJfkepctznJtsBJPymAJzhhmeT9MFwqbQQvgE 5DHqG94fgPNX54QVuHEkAMrtvXYJ2ph2hS4JzVY4vESEAm9J "
        "5CPJnbQXXWZyU5BKBwrRviq5sNktHYn32rGaPNWyCTqYVowh 5G3j9nuzEgLF5mAega9xQWsfEhq7m3jXkuLuSwBeTJYWECfA "
        "5F6vjRj1ZqYswpDVXwGvXNX9Wa5N9D2htTHJsU7ZsZLFXzu8 5HY8V849JcmTwcCJvq6t1waTbmfdHbWRXkRdo4dP2yqfKSBf "
        "5E2WC93Axc4VTynRBqoh5zkbs1kqykXZvNshyyhUpmNSBJG7 5GsDgsLQYxxdn6o9e1CKR1JTqKsW7fHDrjpsWiTf7WAFPC3o "
        "5HNR6ifJh7b5GvCnWAcMSLoQh4G43shBnKKns5p4DEKfuPLq 5DG4VHT3gKZDEQ3Tx4oVPpejaz64FeDtNPhbAYTLFBmygHUW "
        "5FcY8CUfGVvYYyzVZ2r4GetWLBN2GAr4Ky4odxJtmQbye4Wz 5FvKvxJz1iKCQisuatwWzNdshUULiWMGyzF7J2RPRuz449eo "
        "5Gmr8tvDdQQ4TECrtUfRTHNr8Fu9z5acnYQcWiHjHckRTRsS 5GhLWfykGuSXv9oaMJyacNF45TP3mKr1ivkMfAwpoFuqsb1S "
        "5HbthkVNhiLR35wFfxbN4yK1yNwqAqQAVVS62s4ceefNvw2n 5HQvDhp6c3HjwXuBYLfJB92dMewr56tB6Xukk5dL1NG1DFbp "
        "5H9Lz17rBTdEYS7LCdXg3w1vrMmxpjhhE8Mw2ZLPNZDUphh3 5GF1KCCc8sxhaVsWkZaJR1CXqis2Eo9u1kbfqxDLAyb1eLL4 "
        "5F1hucqLa6DrYRLoyNWLJAcFrgN2ifrLqtuXmTACaBgJ3tza 5HEp14zGbxoutFRGQBMrdHxTVU1w5jrnGeJ3eWKDRe6qrukm "
        "5DU7XMB42qnZF2GxXdkW6Cr8dho734ue1PrfKDBUcUAqEKBY 5Fzy8WMsBkCcMn5Gf9CFXbQrAYmEmepjgRuVU7kEGhfEb4Rh "
        "5GuxieMeeAACQAMjwi4AC6nKFz4H4inZHTjt9u6hBG3Dm2oD 5G7FYjDKbnqSKdbMfVoA86H3Bdyx3GbZ8vbmBFcFnqopJMKz "
        "5GsecT96qyjpRKPVEvS5ANEvGptPAHWsP2m3Nee8wPEJBo72 5DAr1n4kc41bTZLRsMFfooFeacHGXEe7DNe8rFyv3TPkFLQf "
        "5GuvM2FCDPZKB9SisJih6t2ienjZwg1MwWxckefzntj9RnUX 5Gp4z53bMPPoRPsfEwrFPzKipPjkTr8XFQixLcqEURRTRRQ8 "
        "5ELACY4qAdoVkySjBoBMLHe338dGi3fV9FQoZvC5qUu7W24p 5GFGi6ELC9kzCLa2godKaoVCrKZtMvez4EpT7QTFKyyQgLVt "
        "5EWM19AUKEphvECTAk3hMF6Zvkp9ZLtZxc6PkakPoznFa5aC 5CChqsKedYwhgJ9ku8MoBQ2h2UcUXgNd6f8MTdeDAuqtyino "
        "5Di5KkU4AoFaPEaQdRMo6DvhfQ5ZJ17kx2aA5dEHw7kxjDAU 5DkGtfPL2VvLedaVrEb4BadJBMe3vzKSSzYUQQgKxPgUuHp2 "
        "5HTFRZN2azeq82S9Fos66rZ2Z1GKB9nfESzkQZ92y66rB9x2 5CBDcd5233gumVCggSp6yb4AWMvnft4Qapim1nhTpB4pd2CM "
        "5FP8RVi5gchyKvbH1eo4ntpeTPZdfKwTJyGBk6YKujg7dMns 5CM7DYZFri3h47GZsdbWbYPAcSuYdCxJ7gXiZtiqfUmVJtE2 "
        "5DoKo13X6RPk3XFnpEFJZPKVZZwju8fbWPEka3KANYdFFFRQ 5GrgH81iP5eD3m3dxL5kqrG9Dt5NiSCJZaiGqz6JyUEyixSf "
        "5GqF1QHvjzu9Vi7Jc6SWfG3yNNn9qKkoysvZDv54g346zKwx 5E2MF7htsXr4dXdoJS5yTUmfLp6LMkr13S3EdR4mUzokyH7o "
        "5CDP6jVS7Cy9hcWSQSnEy7YKkUYLSKiXYbwkqPDN6Kj7VEiQ 5GxAPx6XZ5x4wGMgFqaoEg6q7A27dRcpcibyFevgQbZYZcrf "
        "5HBCug2QsScJL2dqw6rGPqrrJbNZmHLwHzdBgRSTwZraD4SU 5CAdPfTgZCWwoyKVDVYgnwKAjyXmFSLnDxFiW1QmCALG94MB "
        "5CyNWDt28qEryf37ZApKgPA6zXS6pdVcMxkMjuMJU8Scstrp 5HeEBi9bvJ2dwn8dXN89rDa254bnKr5z8citYhD3udqicnZ1 "
        "5G79Sp3LqJFYdGQ62PVvVrBEVeRiqyRXArVfB535QFWFRn1k 5EPgyPbUs49fAxFHzrgB7KYktkH6EJdTuHNK8RbxRCUCCof7 "
        "5FRpmX8pesi7jTUvbcTSFcXY4DgGHSiDCstsrGxRPJp85aAZ 5Dnk42fQBYepNat6MBwv9RQsPKHwLo5BdTTXb6G8eV8FeMmv "
        "5CPR7RHcHHtkdrqJGXiLi94iWfknb7f7CbvDzyDe6b2J6wDw 5DkSqMkYZTGhSv973JAM9swvGzgeYFxeY5WhrvJwKHR6gg3e "
        "5HfytGTCCyxfRU2Ftcvi1YfGTizvwsCwq8gMpfGa1XJhbtwk 5DUBBm7WzS4FS5Rj74o1Q2QWGEAFSCEKC18urEUN3Lu7GS7q "
        "5HRN5GLXHjuLdpuy1wnqsM2MFDBEffsH2SuKkwr8Hz6DQSck 5CXhDxkV22FAFiDx1EQarVtJ8qz1G52n5Z5ptd84Yw2saLhD "
        "5G9cBNeDmDi1BqFQWj6z4cn9r83LVQvLsUtMEzfQwMsbtPR9 5EntLszo4dRveuHK7MmKxdMZL87oTkmjvNf6VuWkViSDgAbg "
        "5FmyyS5dZnKYYPFweoevVFsFwmKNPcapV5EMerB4ADywK5Qi 5HEuYzyTKnQAx779W9UYNJpSGpjioEF63oVPZNcixV8HvkZn "
        "5DwTUHcc239asj7xWm6zudZ4YdJN1yVp1fcxjgjmEH4yUBDo 5GLWYfcBfUB4fGxMXTD5e1qQDGiGRiwgSq6YEVLwoq2vqbmW "
        "5GsNxXaz23zvwTW79KUmoiws857pgGUpyHgPcL1tjHCMpt84 5CV1pApJjXKELoqRhe68euv5JfNFZgugCFTDcKNm3a2BRPLE "
        "5G1LDxnTJ1JgvaviUZcodaeFYZFYDAWaEPNTPt1ri8U6E8md 5EnFttQYUANAkpqoYCZL1mXhWoA6jvhFLLWR2g4zqNxgMYAe "
        "5DhKVLE5bsg8BYY7QC94AJzGHC1LJQ9oCW4R33GekuVMqDY1 5F4RznJAcqnWGnxS9LCn4udLRbesU1iH7tasLmxSDFKLVksE "
        "5EM1T8iNWfefpwboW6a451E2amsUrdhD6xepA9iBAt12oFys 5CyvNTsdXMkTUxbh3YM1jzzUxtTXf7QuAkzWur2UE37GVFGs "
        "5ERxYp3fmBgWUfgQi7sqXxj1bjA1izhQSx7AJV6Jnke8nyMh 5FvLf8P8DSQTFqnYDuZFTmFry5iWj7McCrh74jJfrjnfVJyC "
        "5GqM7hwHtLc4VFVVXWF3gAtY2UTJJPSe1BGVqG7KRcNbmcnE 5EFgTXoyDxGTvC2v6oHC8SXBg79hVwEvFgNk7LGeNQdknLwz "
        "5HThAqPgVz4zMvtCgDvFcA2VN9YuHYwATdF8VwGcVJS6ToFC 5E81DC8SFDNTG42rytf8HkveFToeNwafjZJfXLY1ZvLtAEg4 "
        "5ChWx1q7dY5B5hB7D5K8xksKQsRGb1YQp1XYgacmh5YguFHY 5DhHWS4CwAdmMFJfGyXuKfJZ3VRrDCApt9eoC2A6HsYyCwdb "
        "5FvhdqRVkfzPYarA1ETzWsm8o67CTJy4LDtRfQGjMVn8hFea 5F9WFdvsNo6moEsZymtAVgKswXHrXm4TCktGg4dnqpC6ss9o "
        "5EUXpQXK424WRseNeA9ckC877KdQRvpdLQj4U2eyPFLUtxj5 5GDxot8vEsd1LdyG9Q6abknLnjzyXWbqezYRTLGUhwnH1wyd "
        "5DkNK5241GGSzK6sYjYVWYwraQvBmqiFkQDDSAQ1SjHtiCqF 5HDnDnySziB2g4W91sFtkmrjromEhhJ1b9U59JT6P7GdiqGa "
        "5DZkBQHSogZNhYuLTvz5ZSYz4hVU8jcav1RWNShwdqyfpfSx 5DUiBk255vgnihBTdAXcrBzqdzpK4s8UCtRGR87bj4MUgZcB "
        "5HdZQMqNZ44oRxHfE4Ga3AFMykjEqwRsHrnYLFRf6UFQoNm4 5HBTQAwhqYn4fXSFrWfRyDkFXT5J178CbUvuK6g9bWwKuQ6Q "
        "5CFzMMPggC9kxiLgYibTDPk5w2JDUgmSdwmqxQD5ykFJXg5K 5D7drqrZ3eLrHdNhJ52d7SLYzSDf1RHqxexB43bXDWgkcXqp "
        "5HbkRap76b3S2nCzCPFbvfEWP2EacvardWubbsorCFCVVAmz 5DiLGj6FfR865roh1bfHR76Av91NajBheca4naaCADapeey6 "
        "5DhV69RTR4yN6onp8cwNu3Mtgr41jXQDy4wjKxEWkhwvTUS6 5EWcjhdA6HToZ2bRab1WCrJcToWMdKYNTcYsiP88tApsL8Gy"
    )
    result = await rpc.query_subtensor(
        hotkeys__.split(" "), "TotalHotkeyStake", "SubtensorModule", block_hash
    )
    return {x: bittensor.Balance.from_rao(y[0].value) for x, y in result.items()}


async def get_balance(block_hash, address: str, rpc: rpc_requests.RPCRequest):
    result = await rpc.query_subtensor([address], "Account", "System", block_hash)
    return result[address][0].value["data"]["free"]


async def main():
    start = time.time()
    # subtensor_ = bittensor.subtensor("test")
    # block_hash = subtensor_.substrate.get_chain_head()
    rpc = rpc_requests.RPCRequest(rpc_requests.CHAIN_ENDPOINT)
    # print("block hash", block_hash)
    async with rpc:
        block_hash = rpc.substrate.get_chain_head()
        results = await asyncio.gather(
            get_delegated("5H11iQ22o3cLLNzE1uwEjHdQgRXpueSPyCBFHAX3VKQiz3v3", rpc),
            root_list(block_hash, rpc),
            get_balance(block_hash, "5H11iQ22o3cLLNzE1uwEjHdQgRXpueSPyCBFHAX3VKQiz3v3", rpc)
        )
    pp(results)
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    asyncio.run(main())