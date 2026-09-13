"""Stockline — inventory portal for a trading-card distributor.

Run with:  streamlit run app.py
"""

import streamlit as st

import data
from theme import ACCENT, DISPLAY, LINE, MONO, MUTED, PAPER, SANS, apply_theme

st.set_page_config(page_title="Stockline · Inventory", page_icon="◧", layout="wide")
apply_theme()

st.session_state.setdefault("role", "Ops Manager")


# --- sidebar brand + footer -------------------------------------------------

def _brand() -> None:
    with st.sidebar:
        st.html(
            f"""
            <div style="display:flex;align-items:center;gap:10px;padding:14px 8px 16px;
                        border-bottom:1px solid rgba(255,255,255,.08);margin-bottom:6px">
              <div style="width:30px;height:30px;border-radius:9px;background:{ACCENT};
                          display:flex;align-items:center;justify-content:center;
                          font:600 12px {MONO};color:#fff">SC</div>
              <div style="line-height:1.15">
                <div style="font:600 14px {DISPLAY};letter-spacing:-.02em;color:#fff">Stockline</div>
                <div style="font:400 10px {MONO};color:#6C7689">cards &amp; collectibles</div>
              </div>
            </div>
            """
        )


def _rail_footer() -> None:
    with st.sidebar:
        st.html(
            f"""
            <div style="padding:12px 10px 6px;margin-top:10px;border-top:1px solid rgba(255,255,255,.08)">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">
                <span style="width:26px;height:26px;border-radius:50%;background:#20242E;color:#fff;
                             font:600 10px/26px {MONO};text-align:center">JS</span>
                <span style="line-height:1.2">
                  <span style="display:block;font:600 12px {SANS};color:#E6E8EE">John Smith</span>
                  <span style="display:block;font:400 10px {MONO};color:#6C7689">{st.session_state.role}</span>
                </span>
              </div>
              <div style="display:flex;align-items:center;gap:7px;font:400 10.5px {MONO};color:#6C7689">
                <span style="width:6px;height:6px;border-radius:50%;background:#3BC08A"></span>
                sync ok · 3 min ago
              </div>
            </div>
            """
        )


# --- quick add --------------------------------------------------------------

@st.dialog("Quick add")
def quick_add() -> None:
    kind = st.selectbox("Record type", ["Product / SKU", "Purchase order", "Supplier", "Cycle count"])
    c1, c2 = st.columns(2)
    if kind == "Product / SKU":
        c1.text_input("SKU", placeholder="PKM-151-02")
        c2.text_input("Product name", placeholder="Pokémon 151 Elite Trainer Box")
        c1.selectbox("Line", sorted(data.inventory().line.unique()))
        c2.number_input("Reorder point", min_value=0, value=12, step=1)
    elif kind == "Purchase order":
        c1.selectbox("Supplier", data.SUPPLIER_NAMES)
        c2.selectbox("Destination", ["Main Warehouse", "Store #1", "Store #2"])
        c1.number_input("Units", min_value=1, value=120, step=12)
        c2.date_input("Expected", data.TODAY)
    elif kind == "Supplier":
        c1.text_input("Supplier name")
        c2.text_input("Orders email", placeholder="orders@example.com")
        c1.number_input("Lead time (days)", min_value=1, value=7)
        c2.selectbox("Terms", ["Net 15", "Net 30", "Net 45", "Prepay"])
    else:
        c1.selectbox("Location", data.LOCATIONS)
        c2.selectbox("Scope", ["Full count", "Low stock only", "Single SKU"])
        st.text_area("Note", placeholder="Counted by …")

    st.html(f'<div style="height:1px;background:{LINE};margin:4px 0 10px"></div>')
    left, right = st.columns([1, 1])
    if left.button("Cancel", use_container_width=True):
        st.rerun()
    if right.button("Create", type="primary", use_container_width=True):
        st.session_state.flash = f"{kind} created"
        st.rerun()


def _topbar() -> None:
    search, spacer, add = st.columns([0.46, 0.34, 0.2], vertical_alignment="center")
    search.text_input(
        "search", placeholder="Search SKU, product, order, supplier…",
        label_visibility="collapsed", key="global_search",
    )
    spacer.html(
        f'<div style="display:flex;align-items:center;gap:7px;font:500 11.5px {SANS};color:{MUTED};'
        f'padding-left:4px"><span style="padding:2px 6px;border:1px solid {LINE};border-radius:6px;'
        f'background:{PAPER};font:500 10px {MONO}">⌘K</span> to jump anywhere</div>'
    )
    if add.button("＋  Quick add", type="primary", use_container_width=True):
        quick_add()
    if flash := st.session_state.pop("flash", None):
        st.toast(flash, icon="✅")
    st.html(f'<div style="height:1px;background:{LINE};margin:6px 0 20px"></div>')


# --- routing ----------------------------------------------------------------

pages = [
    st.Page("views/dashboard.py", title="Dashboard", icon=":material/space_dashboard:", default=True),
    st.Page("views/inventory.py", title="Inventory", icon=":material/inventory_2:"),
    st.Page("views/movements.py", title="Stock movements", icon=":material/swap_horiz:"),
    st.Page("views/purchase_orders.py", title="Purchase orders", icon=":material/receipt_long:"),
    st.Page("views/suppliers.py", title="Suppliers", icon=":material/local_shipping:"),
    st.Page("views/reports.py", title="Reports", icon=":material/insights:"),
    st.Page("views/activity.py", title="Activity log", icon=":material/history:"),
]

_brand()
page = st.navigation(pages)
_rail_footer()
_topbar()
page.run()
