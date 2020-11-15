#!/bin/sh

kill -9 $(ps aux | grep -e "crypto_run.py" | awk '{ print $2 }')
kill -9 $(ps aux | grep -e "gas_run.py" | awk '{ print $2 }')
kill -9 $(ps aux | grep -e "forex_run.py" | awk '{ print $2 }')
kill -9 $(ps aux | grep -e "cfgi_run.py" | awk '{ print $2 }') 
