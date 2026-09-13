import altair as alt
import streamlit as st

import data
from components import kpi_row, page_head, panel_head
from theme import ACCENT, style_chart

mv = data.movements()
trend = data.units_trend(21)

page_head(
    "Operations / Stock movements",
    "Stock movements",
    "Every receipt, sale, transfer and count adjustment, newest first. Filter by type or "
    "location to reconcile a shift.",
)

c1, c2, c3 = st.columns([0.4, 0.36, 0.24], vertical_alignment="bottom")
kinds = c1.segmented_control(
    "Type", ["Receipt", "Sale", "Transfer", "Count adj.", "Return"], selection_mode="multi", key="mv_kind"
)
locs = c2.multiselect("Location", data.LOCATIONS, placeholder="All locations")
window = c3.selectbox("Window", ["Last 24 hours", "Last 3 days", "Last 7 days"], index=2)

view = mv.copy()
if kinds:
    view = view[view.kind.isin(kinds)]
if locs:
    view = view[view.location.isin(locs)]
view = view.head({"Last 24 hours": 20, "Last 3 days": 55, "Last 7 days": len(view)}[window])

inbound = int(view[view.qty > 0].qty.sum())
outbound = int(-view[view.qty < 0].qty.sum())
kpi_row(
    [
        {"label": "Movements", "value": f"{len(view):,}", "delta": window.lower(), "tone": "neutral"},
        {"label": "Units in", "value": f"+{inbound:,}", "delta": "receipts & returns", "tone": "good"},
        {"label": "Units out", "value": f"−{outbound:,}", "delta": "sales & transfers", "tone": "neutral"},
        {"label": "Net change", "value": f"{inbound - outbound:+,}", "delta": "across all locations",
         "tone": "good" if inbound >= outbound else "bad"},
    ]
)

left, right = st.columns([0.58, 0.42], gap="medium")

with left:
    with st.container(border=True):
        panel_head("In vs out", "21 days")
        flow = trend.melt("date", ["received", "shipped"], var_name="dir", value_name="units")
        bars = (
            alt.Chart(flow)
            .mark_bar(size=7, cornerRadiusEnd=3)
            .encode(
                x=alt.X("date:T", title=None, axis=alt.Axis(format="%b %d", tickCount=5, grid=False)),
                y=alt.Y("units:Q", title=None, stack=None),
                color=alt.Color(
                    "dir:N", title=None,
                    scale=alt.Scale(domain=["received", "shipped"], range=[ACCENT, "#D8DBE4"]),
                    legend=alt.Legend(orient="top-right", direction="horizontal"),
                ),
                xOffset=alt.XOffset("dir:N"),
                tooltip=["date:T", "dir:N", "units:Q"],
            )
            .properties(height=210)
        )
        st.altair_chart(style_chart(bars), use_container_width=True)

with right:
    with st.container(border=True):
        panel_head("Mix by type", f"{len(view)} movements")
        mix = view.groupby("kind", as_index=False).agg(n=("qty", "size"))
        donut = (
            alt.Chart(mix)
            .mark_arc(innerRadius=52, stroke="#fff", strokeWidth=2)
            .encode(
                theta=alt.Theta("n:Q"),
                color=alt.Color(
                    "kind:N", title=None,
                    scale=alt.Scale(range=[ACCENT, "#8B85F0", "#C7C3F7", "#E2E4EA", "#B9BDC8"]),
                    legend=alt.Legend(orient="right", labelLimit=120),
                ),
                tooltip=["kind:N", "n:Q"],
            )
            .properties(height=210)
        )
        st.altair_chart(style_chart(donut), use_container_width=True)

with st.container(border=True):
    panel_head("Ledger", "newest first")
    log = view.head(60).copy()
    log["when"] = log.at.dt.strftime("%b %d · %I:%M %p")
    st.dataframe(
        log[["when", "kind", "sku", "product", "location", "qty", "actor"]],
        hide_index=True,
        use_container_width=True,
        height=420,
        column_config={
            "when": st.column_config.TextColumn("Timestamp", width="small"),
            "kind": st.column_config.TextColumn("Type", width="small"),
            "sku": st.column_config.TextColumn("SKU", width="small"),
            "product": st.column_config.TextColumn("Product", width="medium"),
            "location": st.column_config.TextColumn("Location", width="medium"),
            "qty": st.column_config.NumberColumn("Qty", format="%+d", width="small"),
            "actor": st.column_config.TextColumn("By", width="small"),
        },
    )
    st.download_button(
        "Export ledger (CSV)",
        log.to_csv(index=False).encode(),
        file_name="stock-movements.csv",
        mime="text/csv",
    )
