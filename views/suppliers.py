import altair as alt
import streamlit as st

import data
from components import badge, meter, page_head, panel_head
from theme import ACCENT, INK, MONO, MUTED, SANS, style_chart

sup = data.suppliers()
pos = data.purchase_orders()

page_head(
    "Supply chain / Suppliers",
    "Suppliers",
    "Five distributors, ranked by 90-day spend. On-time delivery is measured against the "
    "promised date on each purchase order.",
)

cards = st.columns(len(sup), gap="small")
for col, (_, r) in zip(cards, sup.iterrows()):
    tone = "good" if r.on_time >= 0.9 else "warn" if r.on_time >= 0.8 else "bad"
    open_pos = len(pos[(pos.supplier == r.supplier) & (pos.status != "Draft")])
    with col:
        with st.container(border=True):
            st.html(
                f"""<div style="min-height:150px">
                  <div style="display:flex;align-items:center;justify-content:space-between;gap:8px">
                    <span style="font:600 13.5px/1.3 {SANS};letter-spacing:-.01em;color:{INK}">{r.supplier}</span>
                  </div>
                  <div style="margin:7px 0 12px">{badge(f"{r.on_time:.0%} ON TIME", tone)}</div>
                  <div style="display:flex;flex-direction:column;gap:5px;font:400 11.5px/1.5 {SANS};color:{MUTED}">
                    <span>Lead time <b style="font:600 12px {MONO};color:{INK}">{r.lead_days} d</b></span>
                    <span>SKUs <b style="font:600 12px {MONO};color:{INK}">{r.skus}</b></span>
                    <span>90-day spend <b style="font:600 12px {MONO};color:{INK}">${r.spend_90d:,.0f}</b></span>
                    <span>Terms <b style="font:600 12px {MONO};color:{INK}">{r.terms}</b></span>
                    <span>Open POs <b style="font:600 12px {MONO};color:{INK}">{open_pos}</b></span>
                  </div>
                </div>"""
            )
            if st.button("New order", use_container_width=True, key=f"po_{r.supplier}"):
                st.toast(f"Draft PO started for {r.supplier}", icon="🧾")

left, right = st.columns([0.55, 0.45], gap="medium")

with left:
    with st.container(border=True):
        panel_head("90-day spend", "by supplier")
        bars = (
            alt.Chart(sup)
            .mark_bar(cornerRadiusEnd=4, height=18, color=ACCENT)
            .encode(
                y=alt.Y("supplier:N", sort="-x", title=None, axis=alt.Axis(labelFont="Instrument Sans", labelFontSize=11.5)),
                x=alt.X("spend_90d:Q", title=None, axis=alt.Axis(format="$,.0f", grid=True)),
                tooltip=[alt.Tooltip("supplier:N"), alt.Tooltip("spend_90d:Q", format="$,.0f")],
            )
            .properties(height=190)
        )
        st.altair_chart(style_chart(bars), use_container_width=True)

with right:
    with st.container(border=True):
        panel_head("Reliability", "on-time delivery")
        for _, r in sup.sort_values("on_time", ascending=False).iterrows():
            tone = "good" if r.on_time >= 0.9 else "warn" if r.on_time >= 0.8 else "bad"
            st.html(meter(r.supplier, r.on_time * 100, 100, tone, note=f"{r.on_time:.0%} · {r.lead_days}d"))

with st.container(border=True):
    panel_head("Scorecard", "rolling 90 days")
    scorecard = sup.assign(on_time=(sup.on_time * 100).round(0)).sort_values("spend_90d", ascending=False)
    st.dataframe(
        scorecard,
        hide_index=True,
        use_container_width=True,
        column_config={
            "supplier": st.column_config.TextColumn("Supplier", width="medium"),
            "lead_days": st.column_config.NumberColumn("Lead (d)", width="small"),
            "on_time": st.column_config.ProgressColumn("On time", min_value=0, max_value=100, format="%.0f%%"),
            "skus": st.column_config.NumberColumn("SKUs", width="small"),
            "spend_90d": st.column_config.NumberColumn("Spend", format="$%.0f"),
            "terms": st.column_config.TextColumn("Terms", width="small"),
        },
    )
