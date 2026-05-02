import sys
sys.path.insert(0, '.')
import requests
from config import Config

# Check tether-gold using the coin endpoint instead of simple price
print('=== Checking Tether Gold via Coin endpoint ===')
url = '{}/coins/tether-gold'.format(Config.COINGECKO_URL)
try:
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        data = r.json()
        market_data = data.get('market_data', {})
        current_price = market_data.get('current_price', {})
        usd_price = current_price.get('usd')
        print('Tether-gold price from market_data: ${}'.format(usd_price))
        
        # Also check if there's a conversion rate
        if usd_price:
            # Calculate what 1/4 oz would be in IRR using current USD/IRR
            usd_irr_rate = 1314854.49  # From our earlier logs
            quarter_oz_price = (usd_price / 4) * usd_irr_rate
            print('1/4 oz gold price: ${:,.2f} -> {:,.0f} IRR'.format(usd_price/4, quarter_oz_price))
    else:
        print('Status: {}'.format(r.status_code))
        print('Response: {}'.format(r.text[:200]))
except Exception as e:
    print('Error: {}'.format(e))

# Let's also try to get the price via the contract/ticker endpoint for more accuracy
print('')
print('=== Checking Tether Gold Tickers for Price ===')
url = '{}/coins/tether-gold/tickers'.format(Config.COINGECKO_URL)
try:
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        data = r.json()
        tickers = data.get('tickers', [])
        if tickers:
            # Get the first ticker with a price
            for ticker in tickers[:5]:
                last_price = ticker.get('last')
                if last_price:
                    market_name = ticker.get('market', {}).get('name', 'Unknown')
                    print('Ticker: {} - Last: ${}'.format(market_name, last_price))
                    # Use this price for calculation
                    usd_irr_rate = 1314854.49
                    quarter_oz_price = (float(last_price) / 4) * usd_irr_rate
                    print('  -> 1/4 oz gold price: {:,.0f} IRR'.format(quarter_oz_price))
                    break
        else:
            print('No tickers found')
    else:
        print('Status: {}'.format(r.status_code))
except Exception as e:
    print('Error: {}'.format(e))
