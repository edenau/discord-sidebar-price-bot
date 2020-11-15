"""
Run a Discord sidebar bot that shows the Crypto Fear and Greed Index (CFGI)
"""
# Example:
# python3 cfgi_run.py -l 7 &

from typing import Tuple
def get_index(lengthscale: int = 7,
              verbose: bool = False) -> Tuple[int]:
    """
    Fetch index from Alternative Me API
    """
    import requests
    import time
    r = requests.get('https://api.alternative.me/fng/',
                     params={'limit':lengthscale+1})
    if r.status_code == 200:
        if verbose:
            print('200 OK')
        data = r.json()['data']
        past_indices = [int(dict_['value']) for dict_ in data[1:]]
        return int(data[0]['value']), sum(past_indices)/len(past_indices)
    else:
        if verbose:
            print(r.status_code)
        time.sleep(10)

def main(lengthscale: int = 7,
         verbose: bool = False):
    import yaml
    import discord
    import asyncio

    # 1. Load config
    filename = 'cfgi_config.yaml'
    with open(filename) as f:
        config = yaml.load(f, Loader=yaml.Loader)

    # 2. Connect w the bot
    client = discord.Client()

    async def send_update(now, past, lengthscale):
        nickname = f'😨🤑 {now}'
        status = f'{lengthscale}D-SMA: {round(past,1)}'
        await client.get_guild(config['guildId']).me.edit(nick=nickname)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                               name=status))
        await asyncio.sleep(config['updateFreq']) # in seconds

    @client.event
    async def on_ready():
        """
        When discord client is ready
        """
        while True:
            # 3. Fetch index
            # now is today's index; past is {lengthscale}-day SMA
            now, past = get_index(lengthscale=lengthscale, verbose=verbose)
            # 4. Feed it to the bot
            await send_update(now, past, lengthscale)

    client.run(config['discordBotKey'])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--length',
                        type=int,
                        default=7,
                        help='Specify #-day SMA lengthscale')

    parser.add_argument('-v', '--verbose',
                        action='store_true', # equiv. default is False
                        help='toggle verbose')
    args = parser.parse_args()
    main(lengthscale=args.length,
         verbose=args.verbose)
