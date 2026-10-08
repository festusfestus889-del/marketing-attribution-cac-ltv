import pandas as pd

cust = pd.read_csv("data/raw/customers.csv")
ads = pd.read_csv("data/raw/ads_spend.csv")

# CAC / LTV by channel
summary = cust.groupby('converting_channel').agg(
  customers=('customer_id','count'),
  avg_ltv=('ltv_ngn','mean'),
  avg_cac=('cac_ngn','mean'),
  avg_payback=('payback_months','mean'),
  paying_rate=('is_paying','mean')
).reset_index()

summary['ltv_cac_ratio'] = summary['avg_ltv']/summary['avg_cac']
summary['total_ltv'] = summary['customers']*summary['avg_ltv']
summary = summary.sort_values('ltv_cac_ratio', ascending=False)

# Payback interpretation
summary['verdict'] = summary['ltv_cac_ratio'].apply(
  lambda x: "Scale aggressively" if x>4 else "Scale" if x>3 else "Optimize" if x>2 else "Pause/Review"
)

summary.to_csv("data/processed/cac_ltv.csv", index=False)
print(summary.to_string(index=False))

# Scenario: Reallocate 20% of Facebook budget to Referral
fb_customers = summary[summary.converting_channel=="Facebook Ads"]['customers'].values[0]
ref_ltv_cac = summary[summary.converting_channel=="Referral"]['ltv_cac_ratio'].values[0] if len(summary[summary.converting_channel=="Referral"])>0 else 3.5
fb_ltv_cac = summary[summary.converting_channel=="Facebook Ads"]['ltv_cac_ratio'].values[0]

gain = int((ref_ltv_cac - fb_ltv_cac) * 100000) # illustrative
realloc = pd.DataFrame([{
  'scenario': 'Move 20% Facebook spend → Referral',
  'expected_extra_ltv': gain,
  'reason': f"Referral LTV/CAC {ref_ltv_cac:.1f}x vs Facebook {fb_ltv_cac:.1f}x"
}])
realloc.to_csv("data/processed/reallocation.csv", index=False)
print(f"\nReallocation upside: {realloc.to_string(index=False)}")
