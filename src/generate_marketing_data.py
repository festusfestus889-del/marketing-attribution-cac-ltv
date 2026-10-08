import pandas as pd, numpy as np, os, random
from datetime import timedelta
os.makedirs("data/raw", exist_ok=True)
np.random.seed(42)

channels = ["Facebook Ads","Google Ads","Organic Search","Referral","Email"]
channel_cac_base = {"Facebook Ads":2500,"Google Ads":1800,"Organic Search":400,"Referral":600,"Email":800}
channel_ltv_mult = {"Facebook Ads":1.0,"Google Ads":1.5,"Organic Search":1.8,"Referral":2.2,"Email":1.3}

customers=[]
touchpoints=[]
for i in range(5000):
  # Journey length
  n_touches = np.random.choice([1,2,3,4], p=[0.4,0.3,0.2,0.1])
  journey = np.random.choice(channels, n_touches, p=[0.3,0.25,0.2,0.15,0.1]).tolist()
  convert_channel = journey[-1] # last touch converted

  first_date = pd.Timestamp("2024-01-01") + pd.Timedelta(days=np.random.randint(0,400))

  # CRM data
  ltv = int(np.random.normal(15000,5000) * channel_ltv_mult[convert_channel])
  ltv = max(2000, ltv)
  cac = int(np.random.normal(channel_cac_base[convert_channel], 300))
  tenure = np.random.exponential(8) # months
  paying = random.random() < (0.6 + 0.2*channel_ltv_mult[convert_channel]/2)

  customers.append({
    "customer_id": f"U_{i}",
    "first_seen": first_date,
    "conversion_date": first_date + timedelta(days=n_touches*2),
    "converting_channel": convert_channel,
    "journey": " > ".join(journey),
    "ltv_ngn": ltv,
    "cac_ngn": cac,
    "payback_months": round(cac/(ltv/12) if ltv>0 else 99,1),
    "is_paying": paying,
    "tenure_months": round(tenure,1)
  })

  for step,ch in enumerate(journey):
    touchpoints.append({
      "customer_id": f"U_{i}",
      "touch_order": step+1,
      "channel": ch,
      "timestamp": first_date + timedelta(days=step*2),
      "cost": channel_cac_base[ch]/n_touches if ch in ["Facebook Ads","Google Ads"] else 0
    })

pd.DataFrame(customers).to_csv("data/raw/customers.csv", index=False)
pd.DataFrame(touchpoints).to_csv("data/raw/touchpoints.csv", index=False)
# Ads spend
ads = pd.DataFrame([{"channel":c,"spend_ngn": int(np.random.normal(500000,100000)), "impressions": int(np.random.normal(200000,30000))} for c in channels])
ads.to_csv("data/raw/ads_spend.csv", index=False)
print(f"Generated 5000 customers | Avg LTV ₦{pd.DataFrame(customers)['ltv_ngn'].mean():,.0f} | Avg CAC ₦{pd.DataFrame(customers)['cac_ngn'].mean():,.0f}")
