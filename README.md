# Stockline — inventory portal (Streamlit)

A minimal, modern inventory management portal for a trading-card & collectibles
distributor. Same information architecture as the HTML mockup, rebuilt as a
working Streamlit app: dark navigation rail, light work surface, Space Grotesk /
Instrument Sans / JetBrains Mono type, one indigo accent.

## Current scope — Step 1

This repository is the Step 1 foundation: the full application shell, navigation,
and every view (dashboard, inventory, movements, purchase orders, suppliers,
reports, activity) running against representative demo data. No production data,
persistence, authentication, or real backend mutations are wired up yet — actions
that would hit a database currently confirm via `st.toast` instead.

Chosen as a plain-Python alternative to a React/TypeScript stack specifically to
keep the codebase approachable to read and modify without a frontend build
pipeline.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Layout

```
app.py                  page config, theme, nav rail, top bar, quick-add dialog
theme.py                palette tokens, font loading, the CSS that reskins Streamlit
components.py           KPI strip, status badges, panel heads, list rows, meters
data.py                 cached demo dataset (swap for your API / SQL here)
views/
  dashboard.py          KPIs, 45-day on-hand trend, needs-attention, inbound, live feed
  inventory.py          filterable SKU table + selectable row → adjust / reorder panel
  movements.py          in-vs-out bars, type mix donut, exportable ledger
  purchase_orders.py    order book + per-PO receive / chase actions
  suppliers.py          supplier cards, 90-day spend, reliability meters, scorecard
  reports.py            value by line, velocity-vs-cover bubbles, editable reorder worksheet
  activity.py           append-only audit stream with channel / actor filters
.streamlit/config.toml  light theme, brand colors, font faces
```

## Notes for reuse

- **All styling is in `theme.py`.** Change the tokens at the top and the whole
  portal follows; no per-view CSS.
- **`data.py` is the only place with fake data.** Every function returns a
  DataFrame and is `@st.cache_data`-wrapped, so replacing them with real queries
  needs no UI changes.
- Interactions that would hit a backend (adjust stock, receive a PO, raise
  orders) fire `st.toast` confirmations instead.
- `st.navigation` + `st.Page` drive routing, so the rail order lives in `app.py`.
