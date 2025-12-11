import requests, time, json

def tax_change_sniper():
    print("Base — Tax Change Sniper (catches mid-flight buy/sell tax modifications)")
    # Stores last known tax for each token
    known_taxes = {}

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/pairs/base")
            for pair in r.json().get("pairs", []):
                addr = pair["baseToken"]["address"]
                current_buy_tax = pair.get("buyTax", None)
                current_sell_tax = pair.get("sellTax", None)

                if current_buy_tax is None and current_sell_tax is None:
                    continue

                token_name = pair["baseToken"]["symbol"]
                pair_addr = pair["pairAddress"]

                old = known_taxes.get(addr, (None, None))
                old_buy, old_sell = old

                # First time seeing token
                if old_buy is None:
                    known_taxes[addr] = (current_buy_tax, current_sell_tax)
                    continue

                # Tax changed!
                if current_buy_tax != old_buy or current_sell_tax != old_sell:
                    print(f"TAX SNIPED — DEV JUST CHANGED TAX!\n"
                          f"{token_name}\n"
                          f"Old → Buy: {old_buy or 0}% | Sell: {old_sell or 0}%\n"
                          f"New → Buy: {current_buy_tax or 0}% | Sell: {current_sell_tax or 0}%\n"
                          f"https://dexscreener.com/base/{pair_addr}\n"
                          f"→ This is either a stealth rug or a stealth moon move\n"
                          f"→ Dev just flipped the switch — act fast or get rekt\n"
                          f"{'TAX CHANGED'*12}")

                    known_taxes[addr] = (current_buy_tax, current_sell_tax)

        except:
            pass
        time.sleep(4.2)

if __name__ == "__main__":
    tax_change_sniper()
