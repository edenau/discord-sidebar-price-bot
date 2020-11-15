"""
Run a Discord sidebar bot that shows forex price
"""
# Example:
# python3 forex_run.py -p GBP/HKD &

def get_price(symbol: str,
              base: str,
              verbose: bool = False) -> float:
    """
    Fetch price from exchangeratesapi
    """
    import requests
    r = requests.get('https://api.exchangeratesapi.io/latest',
                     params={'symbols':symbol,
                             'base':base})
    if r.status_code == 200:
        if verbose:
            print('200 OK')
        data = r.json()['rates'][symbol]
        return data
    else:
        if verbose:
            print(r.status_code)
        time.sleep(10)

def main(symbol: str,
         base: str,
         verbose: bool = False) -> None:
    import yaml
    import discord
    import asyncio
    symbol, base = symbol.upper(), base.upper()

    # 1. Load config
    filename = 'forex_config.yaml'
    with open(filename) as f:
        config = yaml.load(f, Loader=yaml.Loader)[f'{base}/{symbol}']

    # 2. Connect w the bot
    client = discord.Client()

    async def send_update(ticker, price, numDecimalPlace=None):
        if numDecimalPlace == 0:
            numDecimalPlace = None # round(2.3, 0) -> 2.0 but we don't want ".0"

        nickname = f'{ticker.upper()} {round(price, numDecimalPlace)}'
        await client.get_guild(config['guildId']).me.edit(nick=nickname)
        await asyncio.sleep(config['updateFreq']) # in seconds

    @client.event
    async def on_ready():
        """
        When discord client is ready
        """
        while True:
            # 3. Fetch price
            price = get_price(symbol=symbol,
                              base=base,
                              verbose=verbose)
            # 4. Feed it to the bot
            await send_update(f'{base}/{symbol}', price, config['decimalPlace'])

    client.run(config['discordBotKey'])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--pair',
                        help='forex pair')

    parser.add_argument('-v', '--verbose',
                        action='store_true', # equiv. default is False
                        help='toggle verbose')
    args = parser.parse_args()
    base, symbol = args.pair.split('/')
    main(symbol=symbol,
         base=base,
         verbose=args.verbose)
