"""
Cache a complete cryptocurrency list from Coingecko
"""
# Example:
# python cache_coingecko.py -v

def main(verbose: bool = False) -> None:
    import json
    import requests

    r = requests.get('https://api.coingecko.com/api/v3/coins/list')
    if r.status_code == 200:
        coinInfoList = r.json()
        if verbose:
            print('200 OK')
    else:
        raise NotImplemented(r.status_code)

    filename = 'crypto_cache.json'
    with open(filename, 'w') as f:
        # overwrite
        json.dump(coinInfoList, f)
        if verbose:
            print(f'Data stored at {filename}')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose',
                        action='store_true', # equiv. default is False
                        help='toggle verbose')
    args = parser.parse_args()
    main(verbose=args.verbose)
