"""
Run a Discord sidebar bot that shows price of a cryptocurrency
"""
# Example:
# python3 crypto_run.py -t BTC &

def get_currencySymbol(currTicker: str) -> str:
    """
    Get currency symbol
    """
    if currTicker.upper() == 'USD':
        return '$'
    elif currTicker.upper() == 'BTC':
        return '₿'
    elif currTicker.upper() == 'ETH':
        return 'Ξ'
    else:
        raise NotImplementedError('Invalid currency symbol')

def resolve_ambiguous_ticker(ticker: str) -> str:
    """
    A bodge to resolve ambiguous tickers
    """
    if ticker == 'UNI':
        return 'UNISWAP'
    elif ticker == 'FTT':
        return 'FTX Token'
    elif ticker == 'XOR':
        return 'Sora'
    elif ticker == 'DEXT':
        return 'DexTools'
    elif ticker == 'NOIA':
        return 'NOIA Network'
    else:
        return ticker

from typing import List
def get_price(id_: str,
              unitList: List[str],
              verbose: bool = False) -> dict:
    """
    Fetch price from CoinGecko API
    """
    import requests
    import time
    while True:
        r = requests.get('https://api.coingecko.com/api/v3/simple/price',
                         params={'ids': id_,
                                 'vs_currencies': ','.join(unitList).lower(), # doesn't need to be in lowercase but just in case
                                 'include_24hr_change': 'true'})
        if r.status_code == 200:
            if verbose:
                print('200 OK')
            return r.json()[id_]
        else:
            if verbose:
                print(r.status_code)
            time.sleep(10)

def main(ticker: str,
         verbose: bool = False) -> None:
    import json, yaml
    import discord
    import asyncio

    # 1. Load config
    filename = 'crypto_config.yaml'
    with open(filename) as f:
        config = yaml.load(f, Loader=yaml.Loader)[ticker.upper()] # Assume tickers in yaml file are in uppercase
        if verbose:
            print(f'{ticker} data loaded from {filename}')

    # 2. Load cache
    filename = 'crypto_cache.json'
    with open(filename, 'r') as f:
        coinInfoList = json.load(f)
        if verbose:
            print(f'Data loaded from {filename}')

    # 3. Extract coin ID
    # ok this is a bodge but it works
    ticker_ = resolve_ambiguous_ticker(ticker)
    for info in coinInfoList:
        if info['symbol'].lower() == ticker_.lower() or info['name'].lower() == ticker_.lower(): # greedy (take the first match)
            id_ = info['id']
            break
    else:
        raise Exception(f'{ticker} is not found in {filename}, re-caching might help.')

    # 4. Connect w the bot
    client = discord.Client()
    numUnit = len(config['priceUnit'])

    async def send_update(priceList, unit, numDecimalPlace=None):
        if numDecimalPlace == 0:
            numDecimalPlace = None # round(2.3, 0) -> 2.0 but we don't want ".0"

        price_now = priceList[unit]
        price_now = round(price_now, numDecimalPlace)
        pct_change = priceList[f'{unit}_24h_change']

        nickname = f'{ticker.upper()} {get_currencySymbol(unit)}{price_now}'
        status = f'{get_currencySymbol(unit)} 24h: {pct_change:.2f}%'
        await client.get_guild(config['guildId']).me.edit(nick=nickname)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                               name=status))
        await asyncio.sleep(config['updateFreq'] / numUnit) # in seconds

    @client.event
    async def on_ready():
        """
        When discord client is ready
        """
        while True:
            # 5. Fetch price
            priceList = get_price(id_, config['priceUnit'], verbose)
            # 6. Feed it to the bot
            # max. 3 priceUnit (tried to avoid using for loop)
            await send_update(priceList, config['priceUnit'][0].lower(), config['decimalPlace'][0])
            if len(config['priceUnit']) >= 2:
                await send_update(priceList, config['priceUnit'][1].lower(), config['decimalPlace'][1])
            if len(config['priceUnit']) >= 3:
                await send_update(priceList, config['priceUnit'][2].lower(), config['decimalPlace'][2])

    client.run(config['discordBotKey'])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--ticker',
                        action='store')
    parser.add_argument('-v', '--verbose',
                        action='store_true', # default is False
                        help='toggle verbose')
    args = parser.parse_args()
    main(ticker=args.ticker,
         verbose=args.verbose)
