import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Inventory — StockFlow",
  description: "Stock levels by warehouse and location.",
};

export default function InventoryPage() {
  return (
    <div className="flex flex-col gap-2">
      <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-50">
        Inventory
      </h1>
      <p className="text-sm text-slate-500 dark:text-slate-400">
        Warehouses, bins, and per-location stock levels land here in Phase 5.
      </p>
    </div>
  );
}
