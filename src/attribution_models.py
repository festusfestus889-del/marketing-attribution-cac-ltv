import pandas as pd
import os
os.makedirs("data/processed", exist_ok=True)

cust = pd.read_csv("data/raw/customers.csv")
touches = pd.read_csv("data/raw/touchpoints.csv")

# 1. Last-touch (default)
last_touch = cust['converting_channel'].value_counts().reset_index()
last_touch.columns=['channel','conversions_last_touch']
last_touch['pct'] = last_touch['conversions_last_touch']/len(cust)*100

# 2. First-touch
firsts = touches[touches.touch_order==1]['channel'].value_counts().reset_index()
firsts.columns=['channel','conversions_first_touch']

# 3. Linear
linear = touches['channel'].value_counts().reset_index()
linear.columns=['channel','touches_linear']
linear['weight'] = linear['touches_linear']/linear['touches_linear'].sum()

# 4. Time-decay (last touch gets more)
touches_sorted = touches.sort_values(['customer_id','touch_order'])
# simple decay: weight = 2^order
touches_sorted['decay_weight'] = 2**touches_sorted['touch_order']
decay = touches_sorted.groupby('channel')['decay_weight'].sum().reset_index().sort_values('decay_weight', ascending=False)

# 5. Data-driven-ish: LTV weighted by channel
ltv_by_channel = cust.groupby('converting_channel')['ltv_ngn'].mean().reset_index().sort_values('ltv_ngn', ascending=False)

# Merge
attrib = pd.merge(last_touch, firsts, on='channel', how='outer').fillna(0)
attrib = pd.merge(attrib, linear[['channel','touches_linear']], on='channel', how='outer').fillna(0)
attrib.to_csv("data/processed/attribution.csv", index=False)

decay.to_csv("data/processed/time_decay.csv", index=False)
ltv_by_channel.to_csv("data/processed/ltv_by_channel.csv", index=False)

print("Attribution Models:")
print(attrib)
print("\nTime-Decay (weighted):")
print(decay)
print("\nLTV by Channel:")
print(ltv_by_channel)
