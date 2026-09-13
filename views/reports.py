import altair as alt
import streamlit as st

import data
from components import kpi_row, page_head, panel_head
from theme import ACCENT, GOOD, INK, MONO, MUTED, SANS, WARN, style_chart

inv = data.inventory()
mix = data.line_mix()
trend = data.units_trend()

page_head(
    "Records / Reports",
    "Reports",
    "Value concentration, sell-through and cover — the three views purchasing actually "
    "uses each Monday.",
)

kpi_row(
    [
        {"label": "Inventory value", "value": f"${inv.value.sum():,.0f}", "delta": "16 tracked SKUs", "tone": "neutral"},
        {"label": "Avg cover", "value": f"{inv.cover_weeks.median():.1f} wks", "delta": "median across SKUs", "tone": "neutral"},
        {"label": "Dead stock", "value": f"${inv[inv.cover_weeks > 8].value.sum():,.0f}", "delta": "cover over 8 weeks", "tone": "warn"},
        {"label": "Weekly velocity", "value": f"{int(inv.velocity.sum()):,} u", "delta": "units leaving per week", "tone": "good"},
    ]
)

left, right = st.columns([0.5, 0.5], gap="medium")

with left:
    with st.container(border=True):
        panel_head("Value by product line", "landed cost")
        bars = (
            alt.Chart(mix)
            .mark_bar(cornerRadiusEnd=4, height=18, color=ACCENT)
            .encode(
                y=alt.Y("line:N", sort="-x", title=None, axis=alt.Axis(labelFont="Instrument Sans", labelFontSize=11.5)),
                x=alt.X("value:Q", title=None, axis=alt.Axis(format="$,.0s")),
                tooltip=[alt.Tooltip("line:N", title="Line"), alt.Tooltip("value:Q", format="$,.0f")],
            )
            .properties(height=230)
        )
        st.altair_chart(style_chart(bars), use_container_width=True)

with right:
    with st.container(border=True):
        panel_head("Velocity vs cover", "bubble = value on hand")
        scatter = (
            alt.Chart(inv)
            .mark_circle(opacity=0.85)
            .encode(
                x=alt.X("velocity:Q", title="Units / week"),
                y=alt.Y("cover_weeks:Q", title="Weeks of cover"),
                size=alt.Size("value:Q", legend=None, scale=alt.Scale(range=[60, 900])),
                color=alt.Color(
                    "status:N", title=None,
                    scale=alt.Scale(domain=["Healthy", "Low", "Out", "Overstock"],
                                    range=[GOOD, WARN, "#B42318", ACCENT]),
                    legend=alt.Legend(orient="top-right", direction="horizontal"),
                ),
                tooltip=["product:N", "velocity:Q", "cover_weeks:Q", alt.Tooltip("value:Q", format="$,.0f")],
            )
            .properties(height=230)
        )
        st.altair_chart(style_chart(scatter), use_container_width=True)

with st.container(border=True):
    panel_head("Received vs shipped", "45 days · all locations")
    flow = trend.melt("date", ["received", "shipped"], var_name="dir", value_name="units")
    area = (
        alt.Chart(flow)
        .mark_line(strokeWidth=2, interpolate="monotone")
        .encode(
            x=alt.X("date:T", title=None, axis=alt.Axis(format="%b %d", tickCount=8, grid=False)),
            y=alt.Y("units:Q", title=None),
            color=alt.Color("dir:N", title=None,
                            scale=alt.Scale(domain=["received", "shipped"], range=[ACCENT, "#9AA1AE"]),
                            legend=alt.Legend(orient="top-right", direction="horizontal")),
            tooltip=["date:T", "dir:N", "units:Q"],
        )
        .properties(height=210)
    )
    st.altair_chart(style_chart(area), use_container_width=True)

with st.container(border=True):
    panel_head("Reorder worksheet", "editable — suggested quantities")
    work = inv[inv.on_hand <= inv.reorder_point * 2][
        ["sku", "product", "on_hand", "reorder_point", "velocity", "cover_weeks"]
    ].copy()
    work["suggested"] = (work.velocity * 4 - work.on_hand).clip(lower=0).astype(int)
    work["approve"] = work.suggested > 0
    edited = st.data_editor(
        work,
        hide_index=True,
        use_container_width=True,
        disabled=["sku", "product", "on_hand", "reorder_point", "velocity", "cover_weeks"],
        column_config={
            "sku": st.column_config.TextColumn("SKU", width="small"),
            "product": st.column_config.TextColumn("Product", width="medium"),
            "on_hand": st.column_config.NumberColumn("On hand", width="small"),
            "reorder_point": st.column_config.NumberColumn("Reorder", width="small"),
            "velocity": st.column_config.NumberColumn("U/wk", width="small"),
            "cover_weeks": st.column_config.NumberColumn("Cover", format="%.1f", width="small"),
            "suggested": st.column_config.NumberColumn("Order qty", min_value=0, step=6, width="small"),
            "approve": st.column_config.CheckboxColumn("Approve", width="small"),
        },
        key="worksheet",
    )
    approved = edited[edited.approve]
    c1, c2 = st.columns([0.7, 0.3], vertical_alignment="center")
    c1.html(
        f'<div style="font:400 12.5px {SANS};color:{MUTED}">'
        f'<b style="color:{INK}">{len(approved)}</b> lines approved · '
        f'<b style="color:{INK}">{int(approved.suggested.sum())}</b> units to order</div>'
    )
    if c2.button("Raise POs", type="primary", use_container_width=True):
        st.toast(f"{len(approved)} draft POs created", icon="🧾")
