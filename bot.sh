#!/bin/sh

python crypto_cache.py

python gas_run.py -s gasnow &
python cfgi_run.py -l 7 &
python crypto_run.py -t BTC &
python crypto_run.py -t ETH &
python crypto_run.py -t YFI &
python forex_run.py -p GBP/HKD &
python forex_run.py -p USD/HKD &
