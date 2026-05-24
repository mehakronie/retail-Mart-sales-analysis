import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Data load karo
df = pd.read_csv('retailmart_sales.csv')

# ============ BASIC CHECK ============
print("Shape:", df.shape)
print("\nColumns:\n", df.columns.tolist())
print("\nPehli 5 rows:\n", df.head())
print("\nData types:\n", df.dtypes)
print("\nMissing values:\n", df.isnull().sum())
print("\nBasic stats:\n", df.describe())
print(df["Store"].nunique())



#task 1
store_revenue = df.groupby('Store')['Revenue'].sum().round(2)

store_revenue = store_revenue.sort_values(ascending=False)

print("Store wise Total Revenue:")
for store, revenue in store_revenue.items():
    print(f"  {store:<12} ₹{revenue:,.2f}")
print(f"\nTop Store: {store_revenue.index[0]}")
print(f"Revenue: ₹{store_revenue.iloc[0]:,.2f}")

#task 2

#PRODUCT WISE REVENUE 
product_revenue = df.groupby('Product_Category')['Revenue'].sum().round()
product_revenue = product_revenue.sort_values(ascending=False)

print("Product wise Total Revenue:")
for product, revenue in product_revenue.items():
    print(f"  {product:<15} ₹{revenue:,.2f}")

print(f"\nTop Product: {product_revenue.index[0]}")
print(f"Revenue: ₹{product_revenue.iloc[0]:,.2f}")
print(f"\nLowest Product: {product_revenue.index[-1]}")
print(f" Revenue: ₹{product_revenue.iloc[-1]:,.2f}")

#task 3 
#month revenue trend
month_order = ['January', 'February', 'March', 'April', 'May', 'June']
monthly_revenue = df.groupby('Month')['Revenue'].sum().round(2)
monthly_revenue = monthly_revenue.reindex(month_order)

print("Monthly Revenue Trend:")
for month, revenue in monthly_revenue.items():
    print(f"{month:<12} ₹{revenue:,.2f}")

print(f"\nBest Month:  {monthly_revenue.idxmax()}")
print(f"Worst Month: {monthly_revenue.idxmin()}")

#task 4 
#discount vs revenue analysis

discount_analysis = df.groupby('Discount_%').agg(
    Total_Revenue    = ('Revenue', 'sum'),
    Average_Revenue  = ('Revenue', 'mean'),
    Total_Orders     = ('Revenue', 'count')
).round(2)

print("Discount vs Revenue Analysis:")
print(discount_analysis)

correlation = df['Discount_%'].corr(df['Revenue'])
print(f"\n Correlation (Discount vs Revenue): {correlation:.2f}")

if correlation > 0:
    print("more discount = more revenue!")
elif correlation < 0:
    print("more discount = less revenue!")
else:
    print("no effect!")

#task 5 customer rating

store_rating = df.groupby('Store')['Customer_Rating'].mean().round(2)
store_rating = store_rating.sort_values(ascending=False)

print("Store wise Average Customer Rating:")
for store, rating in store_rating.items():
    stars = '⭐' * int(rating)
    print(f"  {store:<12} {rating}  {stars}")

print(f"\nBest Rated Store:  {store_rating.index[0]} ({store_rating.iloc[0]})")
print(f"Worst Rated Store: {store_rating.index[-1]} ({store_rating.iloc[-1]})")


#graph
plt.style.use('seaborn-v0_8-whitegrid')

fig, axes = plt.subplots(2, 3, figsize=(13, 10))
fig.suptitle('RetailMart India — Sales Analysis Dashboard', 
              fontsize=20, fontweight='bold', y=1)

colors_blue  = ['#1a6fa8','#2080bf','#2d8fd4','#3a9fe8',
                '#47aff0','#5bbff5','#70cff8','#85dffc']
colors_green = ['#1a7a4a','#2a9a5e','#3ab872','#4ad486',
                '#5aec98','#6af4a8','#7af8b8']

#graph 1 store revenue
bars1 = axes[0,0].bar(store_revenue.index, 
                       store_revenue.values / 1e6,
                       color=colors_blue, edgecolor='white', linewidth=0.5)
axes[0,0].set_title('Store wise Total Revenue', 
                     fontsize=13, fontweight='bold', pad=10)
axes[0,0].set_xlabel('Store', fontsize=10)
axes[0,0].set_ylabel('Revenue (₹ Millions)', fontsize=10)
axes[0,0].tick_params(axis='x', rotation=45, labelsize=8)
for bar in bars1:
    axes[0,0].text(bar.get_x() + bar.get_width()/2,
                   bar.get_height(),
                   f'₹{bar.get_height():.1f}M',
                   ha='center', fontsize=7, fontweight='bold')
    
axes[0,0].set_ylim(0, 20)

#graph 2: product revenue
bars2 = axes[0,1].barh(product_revenue.index,
                        product_revenue.values / 1e6,
                        color=colors_blue[::-1], 
                        edgecolor='white', linewidth=0.8)
axes[0,1].set_title('Product wise Revenue', 
                     fontsize=13, fontweight='bold', pad=10)
axes[0,1].set_xlabel('Revenue (₹ Millions)', fontsize=10)
for bar in bars2:
    axes[0,1].text(bar.get_width() + 0.1,
                   bar.get_y() + bar.get_height()/2,
                   f'₹{bar.get_width():.1f}M',
                   va='center', fontsize=8, fontweight='bold')
axes[0,1].set_xlim(0, 25)

#graph 3: Monthly Trend
axes[0,2].plot(monthly_revenue.index, 
               monthly_revenue.values / 1e6,
               color='#1a6fa8', marker='o', linewidth=2.5, 
               markersize=10, markerfacecolor='white',
               markeredgewidth=2.5)
axes[0,2].fill_between(range(len(monthly_revenue)),
                        monthly_revenue.values / 1e6,
                        alpha=0.1, color='#1a6fa8')
axes[0,2].set_title('Monthly Revenue Trend', 
                     fontsize=13, fontweight='bold', pad=10)
axes[0,2].set_xlabel('Month', fontsize=10)
axes[0,2].set_ylabel('Revenue (₹ Millions)', fontsize=10)
axes[0,2].set_xticks(range(len(monthly_revenue)))
axes[0,2].set_xticklabels(monthly_revenue.index, rotation=45)
for i, val in enumerate(monthly_revenue.values / 1e6):
    axes[0,2].text(i, val + 0.1, f'₹{val:.1f}M',
                   ha='center', fontsize=8, fontweight='bold')
axes[0,2].set_ylim(15, 24)

#graph 4: Discount vs Revenue
discount_rev = df.groupby('Discount_%')['Revenue'].sum() / 1e6
bars4 = axes[1,0].bar(discount_rev.index.astype(str),
                       discount_rev.values,
                       color=colors_green, 
                       edgecolor='white', linewidth=0.8)
axes[1,0].set_title('Discount % vs Total Revenue', 
                     fontsize=13, fontweight='bold', pad=10)
axes[1,0].set_xlabel('Discount %', fontsize=10)
axes[1,0].set_ylabel('Revenue (₹ Millions)', fontsize=10)
for bar in bars4:
    axes[1,0].text(bar.get_x() + bar.get_width()/2,
                   bar.get_height() + 0.2,
                   f'₹{bar.get_height():.1f}M',
                   ha='center', fontsize=8, fontweight='bold')

axes[1,0].set_ylim(0, 35)
#graph 5: Customer Rating
colors_rating = ['#f4a020' if r == store_rating.max() 
                 else '#4a9eda' for r in store_rating.values]
bars5 = axes[1,1].barh(store_rating.index, store_rating.values,
                        color=colors_rating, 
                        edgecolor='white', linewidth=0.8)
axes[1,1].set_title('Store wise Customer Rating', 
                     fontsize=13, fontweight='bold', pad=10)
axes[1,1].set_xlabel('Average Rating ⭐', fontsize=10)
axes[1,1].set_xlim(3.5, 4.1)
for bar in bars5:
    axes[1,1].text(bar.get_width() + 0.01,
                   bar.get_y() + bar.get_height()/2,
                   f'{bar.get_width():.2f}',
                   va='center', fontsize=9, fontweight='bold')
axes[1,1].set_xlim(3.0, 4.5) 
    
#graph 6: Revenue Share Pie
pie_colors = ['#1a6fa8','#2d8fd4','#47aff0','#1a7a4a',
              '#3ab872','#6af4a8']
axes[1,2].pie(product_revenue.values,
               labels=product_revenue.index,
               autopct='%1.1f%%', startangle=140,
               colors=pie_colors,
               wedgeprops={'edgecolor':'white','linewidth':1.5})
axes[1,2].set_title('Product Revenue Share', 
                     fontsize=13, fontweight='bold', pad=10)

plt.tight_layout(pad=3.0)
plt.savefig('retailmart_dashboard_pro.png', 
             dpi=150, bbox_inches='tight')
plt.show()
print("Dashboard is save")