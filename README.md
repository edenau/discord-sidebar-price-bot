# discord-sidebar-price-bot
Inspired by [pipercucu/DiscordSidebarPriceBot](https://github.com/pipercucu/DiscordSidebarPriceBot), 
these Python scripts can run Discord bots that pull live data at intervals and display it on the sidebar of a Discord guild (i.e. server). 
It currently supports:

- **Cryptocurrency price** data (in USD, BTC, and/or ETH) from Coingecko API
- **Gas price** of the Ethereum blockchain (in gwei) from Etherscan API or gasnow API
- **Forex price** from exchangeratesapi
- **Crypto Fear & Greed Index** from Alternate.me API

## Dependencies
Recommended `Python 3.7`, although it should support `Python >=3.5 <=3.9`. Install all dependencies:
```
pip install -r requirements.txt
```

## Test & Run
### Cryptocurrency Price Bot
1. Cache the cryptocurrency ticker list from Coincegko by generating a *crypto_cache.json* file.
```
python cache_coingecko.py -v
```

2. Configure [crypto_config.yaml](crypto_config.yaml) using the template provided. 
It requires a unique Discord bot key and (non-unique) Guild ID per bot.
1 sidebar bot per cryptocurrency (expressed by their ticker e.g. BTC, ETH, YFI). For each cryptocurrency, the price can be shown in USD, BTC, and/or ETH.

3. Sometimes multiple coins or tokens share the same ticker (e.g. UNI). In this case, modify [resolver_ambiguous_ticker()](crypto_run.py#L20) to specify the token you want.

4. Run a cryptocurrency price bot:
```
python crypto_run.py -t BTC
```
Replace the ticker `BTC` with any cryptocurrency you have configured in Step 2.

### Gas Price Bot
1. Configure [gas_config.yaml](gas_config.yaml) using the template provided.
It requires a unique Discord bot key and (non-unique) Guild ID per bot.
It also requires an Etherscan API key if you would like to use Etherscan API.

2. Run a gas price bot using Etherscan API:
```
python gas_run.py -s etherscan
```
Replace `etherscan` with `gasnow` to use Gasnow API (no key required!).

### Forex Price Bot
1. Configure [forex_config.yaml](forex_config.yaml) using the template provided. 
It requires a unique Discord bot key and (non-unique) Guild ID per bot.
1 sidebar bot per forex pair (expressed by their ticker/ticker e.g. GBP/HKD).

2. Run a forex price bot:
```
python forex_run.py -p GBP/HKD
```
Replace `GBP/HKD` with any forex pair you have configured in Step 1.

### Crypto Fear & Greed Index
1. Configure [cfgi_config.yaml](cfgi_config.yaml) using the template provided. 
It requires a unique Discord bot key and (non-unique) Guild ID per bot.

2. Run a bot:
```
python cfgi_run.py
```

## Deploy
Once you are familiar with running a single sidebar bot, you can run multiple bots concurrently by calling `./bot.sh` and kill all bots by calling `./kill.sh`. You might want to modify the commands in `./bot.sh` to suit your own needs.
