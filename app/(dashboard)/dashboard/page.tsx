import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Dashboard — StockFlow",
  description: "Stock value, low-stock alerts, and open orders at a glance.",
};

export default function DashboardPage() {
  return (
    <div className="flex flex-col gap-2">
      <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-50">
        Dashboard
      </h1>
      <p className="text-sm text-slate-500 dark:text-slate-400">
        KPI tiles, movement charts, and low-stock alerts land here in Phase 9.
      </p>
    </div>
  );
}
