import pandas as pd
import numpy as np

np.random.seed(42)

stores = ['Mumbai', 'Delhi', 'Bangalore', 'Jaipur', 'Chennai',
          'Hyderabad', 'Pune', 'Kolkata']

products = ['Electronics', 'Clothing', 'Groceries', 
            'Furniture', 'Toys', 'Sports']

months = ['January', 'February', 'March', 'April', 
          'May', 'June']

rows = []
for _ in range(2000):
    store    = np.random.choice(stores)
    product  = np.random.choice(products)
    month    = np.random.choice(months)
    qty      = np.random.randint(1, 50)
    price    = np.random.uniform(100, 5000)
    discount = np.random.choice([0, 5, 10, 15, 20])
    rating   = round(np.random.uniform(2.5, 5.0), 1)

    final_price = price * (1 - discount/100)
    revenue     = qty * final_price

    rows.append([store, product, month, qty,
                 round(price, 2), discount,
                 round(final_price, 2),
                 round(revenue, 2), rating])

df = pd.DataFrame(rows, columns=[
    'Store', 'Product_Category', 'Month',
    'Quantity', 'Original_Price', 'Discount_%',
    'Final_Price', 'Revenue', 'Customer_Rating'])

df.to_csv('retailmart_sales.csv', index=False)
print("✅ Data ready! retailmart_sales.csv ban gayi!")
print(f"Total rows: {len(df)}")