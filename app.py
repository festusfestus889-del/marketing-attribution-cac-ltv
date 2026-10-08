import streamlit as st, pandas as pd, plotly.express as px
st.set_page_config(layout="wide")
st.title("📊 Multi-Source Marketing Attribution & CAC/LTV")

attrib = pd.read_csv("data/processed/attribution.csv")
cac = pd.read_csv("data/processed/cac_ltv.csv")
ltv_ch = pd.read_csv("data/processed/ltv_by_channel.csv")
realloc = pd.read_csv("data/processed/reallocation.csv")

c1,c2,c3 = st.columns(3)
c1.metric("Avg LTV", f"₦{cac['avg_ltv'].mean():,.0f}")
c2.metric("Avg CAC", f"₦{cac['avg_cac'].mean():,.0f}")
c3.metric("Best Channel", f"{cac.iloc[0]['converting_channel']} ({cac.iloc[0]['ltv_cac_ratio']:.1f}x)")

st.plotly_chart(px.bar(attrib, x='channel', y=['conversions_last_touch','conversions_first_touch'], barmode='group', title="First vs Last Touch Attribution"), use_container_width=True)
st.plotly_chart(px.bar(cac, x='converting_channel', y='ltv_cac_ratio', color='verdict', title="LTV/CAC Ratio by Channel (Golden Metric)"), use_container_width=True)
st.plotly_chart(px.scatter(cac, x='avg_cac', y='avg_ltv', size='customers', color='converting_channel', text='converting_channel', title="CAC vs LTV (size=customers)"), use_container_width=True)

st.subheader("CAC / LTV / Payback by Channel")
st.dataframe(cac)
st.subheader("Reallocation Play")
st.dataframe(realloc)
st.success(f"Recommendation: {cac.iloc[0]['verdict']} {cac.iloc[0]['converting_channel']} — LTV/CAC {cac.iloc[0]['ltv_cac_ratio']:.1f}x, Payback {cac.iloc[0]['avg_payback']:.1f} months")
