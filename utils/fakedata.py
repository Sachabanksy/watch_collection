import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# this should not be taking this long to do 

def generate_watch_data(num_records=100):
    # Watch brands and their typical collections/models

    watch_data = {
        'Rolex': {
            'collections': ['Submariner', 'Daytona', 'DateJust', 'GMT-Master II', 'Day-Date', 'Explorer', 'Air-King'],
            'min_price': 5000,
            'max_price': 100000
        },
        'Patek Philippe': {
            'collections': ['Nautilus', 'Calatrava', 'Aquanaut', 'Grand Complications', 'Golden Ellipse'],
            'min_price': 20000,
            'max_price': 500000
        },
        'Audemars Piguet': {
            'collections': ['Royal Oak', 'Royal Oak Offshore', 'Code 11.59', 'Millenary'],
            'min_price': 15000,
            'max_price': 200000
        },
        'Omega': {
            'collections': ['Speedmaster', 'Seamaster', 'Constellation', 'De Ville'],
            'min_price': 3000,
            'max_price': 50000
        },
        'Cartier': {
            'collections': ['Tank', 'Santos', 'Ballon Bleu', 'Pasha', 'Drive'],
            'min_price': 4000,
            'max_price': 80000
        }
    }

    # Case materials and sizes
    case_materials = ['Stainless Steel', 'Yellow Gold', 'White Gold', 'Rose Gold', 'Platinum', 'Titanium']
    case_sizes = ['36mm', '38mm', '40mm', '41mm', '42mm', '44mm']

    # Condition descriptions
    conditions = ['Excellent', 'Very Good', 'Good', 'Fair']

    # Generate data
    records = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*2)  # Last 2 years

    for _ in range(num_records):
        # Select brand and collection
        brand = random.choice(list(watch_data.keys()))
        collection = random.choice(watch_data[brand]['collections'])
        
        # Generate reference number
        ref_number = f"{random.randint(100000, 999999)}"
        
        # Generate year of manufacture
        year = random.randint(1950, 2024)
        
        # Generate price details
        base_price = random.randint(watch_data[brand]['min_price'], watch_data[brand]['max_price'])
        estimate_low = int(base_price * 0.9)
        estimate_high = int(base_price * 1.1)
        
        # Determine if sold and final price
        sold = random.choice([True, False])
        if sold:
            # Sometimes watches go for well above or below estimate
            price_multiplier = random.uniform(0.7, 1.5)
            sold_price = int(base_price * price_multiplier)
        else:
            sold_price = None

        if sold_price: 
            previous_price = sold_price / np.random.choice(range(1, 4))  # This will choose from [1, 2, 3]
        else: 
            previous_price = None
        # Generate auction date
        auction_date = start_date + timedelta(days=random.randint(0, 365*2))
        
        # Generate additional details
        has_box = random.choice([True, False])
        has_papers = random.choice([True, False])
        condition = random.choice(conditions)
        case_material = random.choice(case_materials)
        case_size = random.choice(case_sizes)

        # we also need to add place holder images 
        image = 'https://imageplaceholder.net/300'
        
        if sold_price is not None:
            if sold_price > estimate_high:
                estimate = 'higher'
            elif sold_price < estimate_low:
                estimate = 'lower'
            else:
                estimate = 'wthin estimate'
        else: 
            estimate = None

        record = {
            'brand': brand,
            'collection': collection,
            'reference': ref_number,
            'case_material': case_material,
            'case_size': case_size,
            'year': year,
            'condition': condition,
            'estimate_low': estimate_low,
            'estimate_high': estimate_high,
            'sold': sold,
            'sold_price': sold_price,
            'auction_date': auction_date.strftime('%Y-%m-%d'),
            'has_box': has_box,
            'has_papers': has_papers,
            'lot_number': random.randint(1, 500),
            'movement': 'Automatic' if random.random() > 0.2 else 'Manual',
            'dial_color': random.choice(['Black', 'White', 'Blue', 'Silver', 'Champagne']),
            'auction_house': random.choice(['Christie\'s', 'Sotheby\'s', 'Phillips', 'Bonhams', 'Antiquorum']),
            'image': image,
            'estimate': estimate,
            'previous_price': previous_price
        }
        records.append(record)

    return pd.DataFrame(records)

def read_fake_data():
    df = pd.read_parquet('/Users/sachabanks/Desktop/data-dudes-dash/data/fakedata.parquet')
    return df