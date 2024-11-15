import pandas as pd
import os 
import sys
import random
from datetime import timedelta, datetime
import string

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.fakedata import generate_watch_data

df1 = generate_watch_data(10)

file_path = '/Users/sachabanks/Desktop/data-dudes-dash/data/test-dataset.parquet'

df = pd.read_parquet(file_path)
# Function to generate random data for different data types
def generate_random_data(dtype):
    if dtype == 'object':
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    elif dtype == 'int64':
        return random.randint(1, 1000)
    elif dtype == 'float64':
        return random.uniform(1.0, 1000.0)
    elif dtype == 'bool':
        return random.choice([True, False])
    elif dtype == 'datetime64[ns]':
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*2)  # Last 2 years
        return start_date + timedelta(days=random.randint(0, 365*2))
    else:
        return None

# Function to generate specific fake data for the auction columns
def generate_auction_data(df):
    auction_dates = []
    auction_houses = []
    estimate_lows = []
    estimate_highs = []
    sold_prices = []
    
    for _ in range(len(df)):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*2)  # Last 2 years
        auction_date = start_date + timedelta(days=random.randint(0, 365*2))
        auction_date_str = auction_date.strftime('%Y-%m-%d')
        auction_dates.append(auction_date_str)
        
        auction_house = random.choice(['Christie\'s', 'Sotheby\'s', 'Phillips', 'Bonhams', 'Antiquorum'])
        auction_houses.append(auction_house)
        
        # Assuming brand is a column in df and has 'min_price' and 'max_price' attributes
        brand = df.at[_, 'brand']
        if brand not in brand_prices:
            min_price = random.randint(1000, 5000)
            max_price = min_price + random.randint(1000, 5000)
            brand_prices[brand] = {'min_price': min_price, 'max_price': max_price}
        
        base_price = random.randint(brand_prices[brand]['min_price'], brand_prices[brand]['max_price'])
        estimate_low = int(base_price * 0.9)
        estimate_lows.append(estimate_low)
        
        estimate_high = int(base_price * 1.1)
        estimate_highs.append(estimate_high)
        
        price_multiplier = random.uniform(0.7, 1.5)
        sold_price = int(base_price * price_multiplier)
        sold_prices.append(sold_price)
    
    return auction_dates, auction_houses, estimate_lows, estimate_highs, sold_prices

# Dictionary to store min and max prices for each brand
brand_prices = {}

# Get columns in df1 that are not in df
missing_columns = df1.columns.difference(df.columns)

# Add missing columns to df with random data
for column in missing_columns:
    dtype = df1[column].dtype
    df[column] = [generate_random_data(dtype) for _ in range(len(df))]

# Generate specific fake data for auction columns
auction_dates, auction_houses, estimate_lows, estimate_highs, sold_prices = generate_auction_data(df)

# Add specific fake data to the DataFrame
df['auction_date'] = auction_dates
df['auction_house'] = auction_houses
df['estimate_low'] = estimate_lows
df['estimate_high'] = estimate_highs
df['sold_price'] = sold_prices

print(df.columns)

df.to_parquet('/Users/sachabanks/Desktop/data-dudes-dash/data/fakedata.parquet', index=False)


