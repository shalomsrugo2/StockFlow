import streamlit as st

import data
from components import badge, kpi_row, meter, page_head, panel_head
from theme import INK, LINE, MONO, MUTED, SANS

inv = data.inventory()

page_head(
    "Operations / Inventory",
    "Inventory",
    "Every SKU with on-hand, committed and available counts. Select a row to adjust stock "
    "or raise a purchase order against it.",
)

f1, f2, f3 = st.columns([0.34, 0.34, 0.32], vertical_alignment="bottom")
status = f1.segmented_control(
    "Status", ["All", "Low", "Out", "Overstock"], default="All", key="inv_status"
) or "All"
lines = f2.multiselect("Product line", sorted(inv.line.unique()), placeholder="All lines")
query = f3.text_input("Find", placeholder="SKU or product name")

view = inv.copy()
if status != "All":
    view = view[view.status == status]
if lines:
    view = view[view.line.isin(lines)]
if query:
    q = query.lower()
    view = view[view.sku.str.lower().str.contains(q) | view["product"].str.lower().str.contains(q)]

kpi_row(
    [
        {"label": "SKUs shown", "value": f"{len(view):,}", "delta": f"of {len(inv):,} tracked", "tone": "neutral"},
        {"label": "Units", "value": f"{int(view.on_hand.sum()):,}", "delta": f"{int(view.committed.sum()):,} committed", "tone": "neutral"},
        {"label": "Value", "value": f"${view.value.sum():,.0f}", "delta": "at last landed cost", "tone": "neutral"},
        {"label": "Needs reorder", "value": f"{int((view.on_hand <= view.reorder_point).sum())}", "delta": "below reorder point", "tone": "warn"},
    ]
)

with st.container(border=True):
    panel_head("SKU list", f"{len(view)} rows · sorted by cover")
    table = view.sort_values("cover_weeks")[
        ["sku", "product", "line", "location", "on_hand", "committed", "available", "cover_weeks", "value", "status"]
    ]
    event = st.dataframe(
        table,
        hide_index=True,
        use_container_width=True,
        height=430,
        on_select="rerun",
        selection_mode="single-row",
        key="inv_table",
        column_config={
            "sku": st.column_config.TextColumn("SKU", width="small"),
            "product": st.column_config.TextColumn("Product", width="medium"),
            "line": st.column_config.TextColumn("Line", width="small"),
            "location": st.column_config.TextColumn("Location", width="medium"),
            "on_hand": st.column_config.NumberColumn("On hand", width="small"),
            "committed": st.column_config.NumberColumn("Cmtd", width="small"),
            "available": st.column_config.NumberColumn("Avail", width="small"),
            "cover_weeks": st.column_config.ProgressColumn(
                "Cover (wks)", min_value=0, max_value=12, format="%.1f", width="small"
            ),
            "value": st.column_config.NumberColumn("Value", format="$%.0f", width="small"),
            "status": st.column_config.TextColumn("Status", width="small"),
        },
    )

picked = event.selection.rows if event and event.selection else []
if picked:
    r = table.iloc[picked[0]]
    tone = {"Out": "bad", "Low": "warn", "Overstock": "accent"}.get(r.status, "good")
    with st.container(border=True):
        st.html(
            f"""<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:4px">
              <div>
                <div style="font:400 10.5px {MONO};letter-spacing:.1em;color:{MUTED}">{r.sku} · {r.line}</div>
                <div style="margin-top:6px;font:600 19px {SANS};letter-spacing:-.02em;color:{INK}">{r['product']}</div>
                <div style="margin-top:5px;font:400 12.5px {SANS};color:{MUTED}">{r.location}</div>
              </div>
              <div>{badge(r.status.upper(), tone)}</div>
            </div>"""
        )
        a, b = st.columns([0.55, 0.45], gap="medium")
        with a:
            st.html(meter("On hand vs reorder point", r.on_hand, max(r.on_hand, view.reorder_point.max()), tone,
                          note=f"{r.on_hand} / reorder {int(inv.loc[inv.sku == r.sku, 'reorder_point'].iloc[0])}"))
            st.html(meter("Weeks of cover", min(r.cover_weeks, 12), 12, "accent", note=f"{r.cover_weeks} wks"))
            st.html(
                f"""<div style="display:flex;gap:22px;margin-top:6px">
                  <span style="font:400 11.5px {SANS};color:{MUTED}">Available<br>
                    <b style="font:600 15px {MONO};color:{INK}">{int(r.available)}</b></span>
                  <span style="font:400 11.5px {SANS};color:{MUTED}">Committed<br>
                    <b style="font:600 15px {MONO};color:{INK}">{int(r.committed)}</b></span>
                  <span style="font:400 11.5px {SANS};color:{MUTED}">Value<br>
                    <b style="font:600 15px {MONO};color:{INK}">${r.value:,.0f}</b></span>
                </div>"""
            )
        with b:
            st.html(f'<div style="font:500 10.5px {MONO};letter-spacing:.1em;color:{MUTED};margin-bottom:6px">ADJUST STOCK</div>')
            delta = st.number_input("Delta", value=0, step=1, label_visibility="collapsed")
            reason = st.selectbox("Reason", ["Cycle count", "Damage / write-off", "Found stock", "Transfer in"])
            c1, c2 = st.columns(2)
            if c1.button("Apply", type="primary", use_container_width=True):
                st.toast(f"{r.sku}: {delta:+d} units — {reason.lower()}", icon="✅")
            if c2.button("Reorder", use_container_width=True):
                st.toast(f"Draft PO opened for {r.sku}", icon="🧾")
else:
    st.html(
        f'<div style="border:1px dashed {LINE};border-radius:12px;padding:16px 18px;'
        f'font:400 12.5px {SANS};color:{MUTED}">Select a row to open the SKU detail panel.</div>'
    )
