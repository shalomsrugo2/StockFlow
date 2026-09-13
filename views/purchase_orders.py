import streamlit as st

import data
from components import badge, kpi_row, meter, page_head, panel_head
from theme import INK, MONO, MUTED, SANS

pos = data.purchase_orders()
TONE = {"Late": "bad", "Receiving": "warn", "In transit": "accent", "Draft": "neutral"}

page_head(
    "Supply chain / Purchase orders",
    "Purchase orders",
    "Eight orders in flight across five distributors. Late orders are held at the top — "
    "open one to receive against it.",
)

kpi_row(
    [
        {"label": "Open orders", "value": f"{len(pos[pos.status != 'Draft'])}", "delta": "2 arriving this week", "tone": "neutral"},
        {"label": "Units inbound", "value": f"{int(pos[pos.status != 'Draft'].units.sum()):,}", "delta": "committed to POs", "tone": "neutral"},
        {"label": "Open commitment", "value": f"${pos[pos.status != 'Draft'].value.sum():,.0f}", "delta": "at agreed cost", "tone": "neutral"},
        {"label": "Late", "value": f"{len(pos[pos.status == 'Late'])}", "delta": f"{int(pos[pos.status == 'Late'].units.sum())} units delayed", "tone": "bad"},
    ]
)

f1, f2 = st.columns([0.5, 0.5], vertical_alignment="bottom")
status = f1.segmented_control("Status", ["All", "Late", "In transit", "Receiving", "Draft"], default="All") or "All"
supplier = f2.multiselect("Supplier", data.SUPPLIER_NAMES, placeholder="All suppliers")

view = pos.copy()
if status != "All":
    view = view[view.status == status]
if supplier:
    view = view[view.supplier.isin(supplier)]
view = view.sort_values("due_in")

with st.container(border=True):
    panel_head("Order book", f"{len(view)} orders")
    table = view.copy()
    table["due_str"] = table.due.apply(lambda d: d.strftime("%b %d"))
    st.dataframe(
        table[["po", "supplier", "destination", "lines", "units", "value", "due_str", "status"]],
        hide_index=True,
        use_container_width=True,
        column_config={
            "po": st.column_config.TextColumn("PO", width="small"),
            "supplier": st.column_config.TextColumn("Supplier", width="medium"),
            "destination": st.column_config.TextColumn("Destination", width="medium"),
            "lines": st.column_config.NumberColumn("Lines", width="small"),
            "units": st.column_config.NumberColumn("Units", width="small"),
            "value": st.column_config.NumberColumn("Value", format="$%.0f", width="small"),
            "due_str": st.column_config.TextColumn("Due", width="small"),
            "status": st.column_config.TextColumn("Status", width="small"),
        },
    )

st.html(f'<div style="height:2px"></div>')

for _, r in view.head(4).iterrows():
    with st.expander(f"{r.po} — {r.supplier} · {r.units} units · {r.status}"):
        head, act = st.columns([0.6, 0.4], gap="medium")
        with head:
            st.html(
                f"""<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
                      {badge(r.status.upper(), TONE.get(r.status, 'neutral'))}
                      <span style="font:400 11px {MONO};color:{MUTED}">due {r.due.strftime('%b %d, %Y')} ·
                      {r.lines} lines · ${r.value:,.0f}</span>
                    </div>"""
            )
            received = 0 if r.status in ("Draft", "In transit") else int(r.units * 0.4)
            st.html(meter("Received against order", received, r.units, TONE.get(r.status, "accent"),
                          note=f"{received} / {r.units} units"))
            st.html(
                f'<div style="font:400 12.5px/1.6 {SANS};color:{MUTED}">Destination '
                f'<b style="color:{INK}">{r.destination}</b> · terms per supplier agreement · '
                f'landed cost recalculated on receipt.</div>'
            )
        with act:
            qty = st.number_input("Receive units", min_value=0, max_value=int(r.units),
                                  value=int(r.units), step=6, key=f"recv_{r.po}")
            loc = st.selectbox("Put away to", data.LOCATIONS, key=f"loc_{r.po}")
            b1, b2 = st.columns(2)
            if b1.button("Receive", type="primary", use_container_width=True, key=f"go_{r.po}"):
                st.toast(f"{r.po}: received {qty} units to {loc}", icon="📦")
            if b2.button("Chase", use_container_width=True, key=f"chase_{r.po}"):
                st.toast(f"Reminder emailed to {r.supplier}", icon="✉️")
