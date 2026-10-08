# Multi-Source Marketing Attribution & CAC/LTV by Channel

**Problem:** 5 channels, conflicting attribution, need true CAC and payback.

**Pipeline:**
1. Generated 5000 journeys (Ads spend + Web touches + CRM LTV) across Facebook, Google, Organic, Referral, Email
2. Attribution: Last-touch vs First-touch vs Linear vs Time-decay (2^order) → Referral overvalued by last-touch
3. CAC/LTV: Referral LTV/CAC 4.8x (payback 2.1mo) vs Facebook 2.1x (payback 5.8mo) → Organic best long-term
4. Scenario: Move 20% Facebook → Referral = +₦1.2M LTV lift
5. Verdict: Scale Referral + Organic, Optimize Google, Review Facebook

**Stack:** Python, Pandas, Scikit-learn, Plotly, Streamlit, GitHub Actions (daily 8am)

**Run:** streamlit run app.py
