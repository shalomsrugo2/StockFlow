"""Demo dataset: a trading-card & collectibles distributor.

Deterministic fake data so the portal reads like a real operation. Swap these
functions for your warehouse API / SQL queries and the UI is unchanged.
"""

from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd
import streamlit as st

TODAY = dt.date(2026, 9, 13)

LOCATIONS = ["Main Warehouse · A", "Main Warehouse · B", "Store #1 · Floor", "Store #2 · Case"]
SUPPLIER_NAMES = [
    "Cardline Wholesale",
    "Southern Hobby",
    "GTS Distribution",
    "ABC Distribution",
    "Pacific Collectibles",
]

_CATALOG = [
    # sku, name, set/line, location, on_hand, committed, reorder_point, unit_cost
    ("PKM-151-01", "Pokémon 151 Booster Bundle", "Pokémon TCG", 0, 3, 0, 10, 44.95),
    ("PRE-ETB-02", "Prismatic Evolutions ETB", "Pokémon TCG", 0, 96, 12, 40, 48.00),
    ("SVI-BB-03", "Scarlet & Violet Booster Box", "Pokémon TCG", 1, 412, 36, 80, 112.00),
    ("MEGA-01", "Mega Evolution Pack", "Pokémon TCG", 0, 0, 0, 8, 27.50),
    ("OBS-TIN-04", "Obsidian Flames Tin", "Pokémon TCG", 2, 0, 0, 12, 21.00),
    ("TPC-24-HB", "Topps Chrome Hobby Box", "Baseball", 3, 4, 1, 15, 279.00),
    ("OPT-25-BX", "Donruss Optic Blaster", "Basketball", 2, 6, 2, 12, 29.99),
    ("PAN-PR-09", "Panini Prizm Retail Box", "Basketball", 1, 128, 8, 60, 64.00),
    ("MTG-LCI-BB", "Lost Caverns Bundle", "Magic: The Gathering", 1, 74, 6, 30, 39.50),
    ("MTG-MH3-CB", "Modern Horizons 3 Collector", "Magic: The Gathering", 0, 18, 4, 24, 284.00),
    ("YGO-QCR-BX", "Quarter Century Rarity Box", "Yu-Gi-Oh!", 3, 52, 3, 25, 41.00),
    ("PSA-GRD-10", "PSA 10 Graded Singles (lot)", "Graded", 2, 31, 5, 15, 186.00),
    ("ONE-OP07-BX", "OP-07 Booster Box", "One Piece", 1, 8, 2, 20, 96.00),
    ("LOR-S5-BX", "Lorcana Set 5 Booster Box", "Disney Lorcana", 0, 140, 10, 50, 108.00),
    ("SUP-SLV-100", "Card Sleeves (100ct, matte)", "Supplies", 3, 960, 40, 300, 3.85),
    ("SUP-TLD-50", "Top Loaders (50ct)", "Supplies", 2, 180, 22, 200, 6.40),
]


def _status(on_hand: int, reorder: int) -> str:
    if on_hand == 0:
        return "Out"
    if on_hand <= reorder:
        return "Low"
    if on_hand > reorder * 4:
        return "Overstock"
    return "Healthy"


@st.cache_data
def inventory() -> pd.DataFrame:
    df = pd.DataFrame(
        _CATALOG,
        columns=["sku", "product", "line", "loc", "on_hand", "committed", "reorder_point", "unit_cost"],
    )
    df["location"] = [LOCATIONS[i] for i in df.pop("loc")]
    df["available"] = df.on_hand - df.committed
    df["value"] = (df.on_hand * df.unit_cost).round(2)
    df["status"] = [_status(h, r) for h, r in zip(df.on_hand, df.reorder_point)]
    rng = np.random.default_rng(7)
    df["velocity"] = rng.integers(2, 46, len(df))  # units/week
    df["cover_weeks"] = (df.available / df.velocity).round(1)
    return df


@st.cache_data
def purchase_orders() -> pd.DataFrame:
    rows = [
        ("PO-1047", "Cardline Wholesale", "Main Warehouse", 6, 288, 11_232, 4, "In transit"),
        ("PO-1046", "Pacific Collectibles", "Store #2", 3, 84, 5_376, 2, "In transit"),
        ("PO-1045", "Southern Hobby", "Main Warehouse", 7, 204, 7_752, 9, "Draft"),
        ("PO-1044", "Cardline Wholesale", "Main Warehouse", 5, 96, 3_648, 6, "Draft"),
        ("PO-1042", "Southern Hobby", "Main Warehouse", 4, 240, 9_120, 0, "Receiving"),
        ("PO-1041", "GTS Distribution", "Store #1", 4, 144, 5_472, -1, "Late"),
        ("PO-1038", "GTS Distribution", "Store #1", 4, 144, 5_472, -3, "Late"),
        ("PO-1031", "Cardline Wholesale", "Main Warehouse", 9, 612, 23_256, -4, "Late"),
    ]
    df = pd.DataFrame(rows, columns=["po", "supplier", "destination", "lines", "units", "value", "due_in", "status"])
    df["due"] = [TODAY + dt.timedelta(days=int(d)) for d in df.due_in]
    return df


@st.cache_data
def movements(n: int = 120) -> pd.DataFrame:
    rng = np.random.default_rng(21)
    inv = inventory()
    kinds = np.array(["Receipt", "Sale", "Transfer", "Count adj.", "Return"])
    weights = [0.22, 0.46, 0.14, 0.1, 0.08]
    picks = rng.choice(len(inv), n)
    kind = rng.choice(kinds, n, p=weights)
    qty = rng.integers(1, 60, n)
    sign = np.where(np.isin(kind, ["Receipt", "Return"]), 1, -1)
    stamps = [
        dt.datetime.combine(TODAY, dt.time(9, 0))
        - dt.timedelta(minutes=int(m))
        for m in np.cumsum(rng.integers(18, 260, n))
    ]
    return pd.DataFrame(
        {
            "at": stamps,
            "kind": kind,
            "sku": inv.sku.values[picks],
            "product": inv["product"].values[picks],
            "location": inv.location.values[picks],
            "qty": qty * sign,
            "actor": rng.choice(["J. Smith", "S. Moreno", "D. Okafor", "auto:shopify", "auto:reorder"], n),
        }
    )


@st.cache_data
def suppliers() -> pd.DataFrame:
    rows = [
        ("Cardline Wholesale", 7, 0.96, 214, 38_136, "Net 30"),
        ("Southern Hobby", 5, 0.91, 168, 26_872, "Net 30"),
        ("GTS Distribution", 12, 0.72, 96, 11_944, "Net 15"),
        ("ABC Distribution", 9, 0.88, 54, 7_320, "Prepay"),
        ("Pacific Collectibles", 4, 0.98, 41, 9_880, "Net 45"),
    ]
    return pd.DataFrame(rows, columns=["supplier", "lead_days", "on_time", "skus", "spend_90d", "terms"])


@st.cache_data
def units_trend(days: int = 45) -> pd.DataFrame:
    rng = np.random.default_rng(3)
    base = 11_600
    walk = np.cumsum(rng.normal(28, 130, days)).round()
    dates = [TODAY - dt.timedelta(days=days - 1 - i) for i in range(days)]
    received = rng.integers(0, 420, days)
    shipped = rng.integers(60, 380, days)
    return pd.DataFrame({"date": dates, "units": base + walk, "received": received, "shipped": shipped})


@st.cache_data
def line_mix() -> pd.DataFrame:
    inv = inventory()
    g = inv.groupby("line", as_index=False).agg(units=("on_hand", "sum"), value=("value", "sum"))
    return g.sort_values("value", ascending=False)


@st.cache_data
def activity(n: int = 26) -> pd.DataFrame:
    events = [
        ("Import", "catalog-sep-12.csv failed — 7 rows rejected", "bad"),
        ("Reorder", "MEGA-01 hit zero on hand at Store #1", "bad"),
        ("Purchasing", "PO-1038 from GTS Distribution is 3 days overdue", "warn"),
        ("Receiving", "Received 48 units against PO-1042", "good"),
        ("Pricing", "Bulk price update applied to 18 Pokémon SKUs", "accent"),
        ("Cycle count", "Store #2 · Case 3 variance −4 units", "warn"),
        ("Integration", "Shopify sync completed — 312 orders", "good"),
        ("Access", "D. Okafor granted Receiving role", "neutral"),
    ]
    rng = np.random.default_rng(11)
    picks = rng.integers(0, len(events), n)
    mins = np.cumsum(rng.integers(9, 190, n))
    return pd.DataFrame(
        {
            "at": [dt.datetime.combine(TODAY, dt.time(9, 20)) - dt.timedelta(minutes=int(m)) for m in mins],
            "channel": [events[i][0] for i in picks],
            "detail": [events[i][1] for i in picks],
            "tone": [events[i][2] for i in picks],
            "actor": rng.choice(["J. Smith", "S. Moreno", "D. Okafor", "system"], n),
        }
    )


def ago(stamp: dt.datetime) -> str:
    delta = dt.datetime.combine(TODAY, dt.time(9, 30)) - stamp
    mins = int(delta.total_seconds() // 60)
    if mins < 60:
        return f"{max(mins, 1)} min ago"
    if mins < 60 * 24:
        return f"{mins // 60} hr ago"
    return f"{mins // (60 * 24)} d ago"
