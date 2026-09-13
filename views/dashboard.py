import altair as alt
import streamlit as st

import data
from components import kpi_row, meter, page_head, panel_head, rows
from theme import ACCENT, GOOD, INK, LINE, MONO, MUTED, SANS, style_chart

inv = data.inventory()
pos = data.purchase_orders()
trend = data.units_trend()
mv = data.movements()

page_head(
    "Operations / Overview",
    "Good morning, John",
    "12,482 units across two warehouses and two retail floors. Three purchase orders "
    "are late and 22 SKUs are at or below their reorder point.",
)

kpi_row(
    [
        {"label": "Units on hand", "value": "12,482", "delta": "▲ 3.1% vs last week", "tone": "good"},
        {"label": "Inventory value", "value": "$286,420", "delta": "▲ $8,140 this month", "tone": "good"},
        {"label": "Active SKUs", "value": "1,247", "delta": "+12 added this week", "tone": "neutral"},
        {"label": "At / below reorder", "value": "22", "delta": "▲ 6 since Monday", "tone": "warn"},
        {"label": "Late POs", "value": "3", "delta": "612 units delayed", "tone": "bad"},
    ]
)

left, right = st.columns([0.63, 0.37], gap="medium")

with left:
    with st.container(border=True):
        panel_head("Units on hand", "45 days · all locations")
        area = (
            alt.Chart(trend)
            .mark_area(
                line={"color": ACCENT, "strokeWidth": 2},
                color=alt.Gradient(
                    gradient="linear",
                    stops=[
                        alt.GradientStop(color="#EEEDFD", offset=0),
                        alt.GradientStop(color="#FFFFFF", offset=1),
                    ],
                    x1=1, x2=1, y1=1, y2=0,
                ),
            )
            .encode(
                x=alt.X("date:T", title=None, axis=alt.Axis(format="%b %d", tickCount=6, grid=False)),
                y=alt.Y("units:Q", title=None, scale=alt.Scale(zero=False, nice=True)),
                tooltip=[alt.Tooltip("date:T", title="Date"), alt.Tooltip("units:Q", title="Units", format=",")],
            )
            .properties(height=196)
        )
        st.altair_chart(style_chart(area), use_container_width=True)

    with st.container(border=True):
        panel_head("Needs attention", action="Open inventory →")
        watch = inv[inv.status.isin(["Out", "Low"])].sort_values(["on_hand", "cover_weeks"]).head(5)
        rows(
            [
                {
                    "title": f"{r['product']}",
                    "meta": f"{r.sku} · {r.location} · reorder at {r.reorder_point}",
                    "value": f"{r.on_hand} on hand",
                    "value_tone": "bad" if r.status == "Out" else "warn",
                    "tail": f"{r.velocity}/wk velocity",
                }
                for _, r in watch.iterrows()
            ]
        )

with right:
    with st.container(border=True):
        panel_head("Stock health", f"{len(inv)} tracked SKUs")
        counts = inv.status.value_counts()
        total = int(counts.sum())
        for label, tone in [("Healthy", "good"), ("Low", "warn"), ("Out", "bad"), ("Overstock", "accent")]:
            n = int(counts.get(label, 0))
            st.html(meter(label, n, total, tone, note=f"{n} SKUs"))

    with st.container(border=True):
        panel_head("Inbound", f"{len(pos[pos.status != 'Draft'])} open POs")
        rows(
            [
                {
                    "title": f"{r.po} · {r.supplier}",
                    "meta": f"{r.destination} · {r.lines} lines",
                    "value": f"{r.units} u",
                    "value_tone": "bad" if r.status == "Late" else "neutral",
                    "tail": r.status if r.status == "Late" else r.due.strftime("%b %d"),
                }
                for _, r in pos[pos.status != "Draft"].head(5).iterrows()
            ]
        )

    with st.container(border=True):
        panel_head("Today", "since 09:00")
        received = int(mv[(mv.kind == "Receipt")].qty.head(12).sum())
        shipped = int(-mv[(mv.kind == "Sale")].qty.head(28).sum())
        st.html(
            f"""<div style="display:flex;gap:10px">
              <div style="flex:1;padding:12px 14px;border:1px solid {LINE};border-radius:11px">
                <div style="font:500 10px {MONO};letter-spacing:.1em;color:{MUTED}">RECEIVED</div>
                <div style="margin-top:8px;font:600 20px {SANS};color:{GOOD};font-variant-numeric:tabular-nums">+{received}</div>
              </div>
              <div style="flex:1;padding:12px 14px;border:1px solid {LINE};border-radius:11px">
                <div style="font:500 10px {MONO};letter-spacing:.1em;color:{MUTED}">SHIPPED</div>
                <div style="margin-top:8px;font:600 20px {SANS};color:{INK};font-variant-numeric:tabular-nums">−{shipped}</div>
              </div>
            </div>"""
        )

with st.container(border=True):
    panel_head("Latest movements", "live feed")
    recent = mv.head(8).copy()
    recent["when"] = recent.at.dt.strftime("%I:%M %p").str.lstrip("0")
    st.dataframe(
        recent[["when", "kind", "sku", "product", "location", "qty", "actor"]],
        hide_index=True,
        use_container_width=True,
        column_config={
            "when": st.column_config.TextColumn("Time", width="small"),
            "kind": st.column_config.TextColumn("Type", width="small"),
            "sku": st.column_config.TextColumn("SKU", width="small"),
            "product": st.column_config.TextColumn("Product", width="medium"),
            "location": st.column_config.TextColumn("Location", width="medium"),
            "qty": st.column_config.NumberColumn("Qty", format="%+d", width="small"),
            "actor": st.column_config.TextColumn("By", width="small"),
        },
    )
