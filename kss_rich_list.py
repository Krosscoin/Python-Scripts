# Provide NODE and API_KEY to file and it'll fetch the rich list of KSS holders. 
# Script stores rich list data in a current directory folder called data and saves the file there as kss_richlist.json and file updates every hour.
# Press Ctrl+C to exit the script.
# Script calculates total_balance, holder_count, last_updated to know when it was last updated.
# To make kss_richlist.json as global data it can be run under screen mode using command python3 -m http.server 8000 

import requests
import sys
import json
import time
import os
from datetime import datetime

# Configuration (hardcoded)
NODE = 'http://127.0.0.1:6869'
API_KEY = ''  # Replace with your API key or set to '' if not required
UPDATE_INTERVAL = 3600  # 1 hour in seconds

def fetch_richlist():
    """Fetch rich list from KSS node."""
    try:
        headers = {"api_key": API_KEY} if API_KEY else {}
        response = requests.get(f'{NODE}/debug/state', headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching rich list: {e}", file=sys.stderr)
        return None

def update_richlist():
    """Update and save the rich list with all addresses."""
    # Fetch rich list
    states = fetch_richlist()
    if not states:
        return False

    # Prepare JSON data
    last_updated = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    holders = []
    total_balance = 0
    n = 0

    # Process rich list
    print("-" * 64)
    print(str.center("KSS Rich List", 64))
    print(f"Last Updated: {last_updated}")
    print("  #    Address                                      Balance")
    print("-" * 64)

    for address, balance in sorted(states.items(), key=lambda x: -x[1]):
        if len(address) == 35 and balance > 0:
            n += 1
            balance_decimal = balance / 1e8
            total_balance += balance_decimal
            holders.append({
                "address": address,
                "balance": balance_decimal
            })
            # Print to console
            print("%6d %-38s %18.8f" % (n, address, balance_decimal))

    print("-" * 64)
    print("                                              %18.8f" % total_balance)

    # Ensure data folder exists
    data_dir = 'data'
    try:
        os.makedirs(data_dir, exist_ok=True)
    except OSError as e:
        print(f"Error creating data folder: {e}", file=sys.stderr)
        return False

    # Write JSON file
    output_file = os.path.join(data_dir, 'kss_richlist.json')
    json_data = {
        "last_updated": last_updated,
        "holders": holders,
        "total_balance": total_balance,
        "holder_count": n
    }
    try:
        with open(output_file, 'w') as f:
            json.dump(json_data, f, indent=2)
        print(f"Rich list saved to {output_file}")
        print(f"To serve the file, run: python -m http.server 8000")
        print(f"Access at: http://your-server-ip:8000/data/kss_richlist.json")
        return True
    except IOError as e:
        print(f"Error writing JSON file: {e}", file=sys.stderr)
        return False

def main():
    print("Starting KSS Rich List generator (updates every hour)...")
    print("Press Ctrl+C to stop")
    
    while True:
        success = update_richlist()
        if not success:
            print("Retrying in 60 seconds...")
            time.sleep(60)
            continue
        
        try:
            print(f"Waiting {UPDATE_INTERVAL} seconds until next update...")
            time.sleep(UPDATE_INTERVAL)
        except KeyboardInterrupt:
            print("\nStopped by user")
            sys.exit(0)

if __name__ == "__main__":
    main()
