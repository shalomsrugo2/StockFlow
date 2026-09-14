import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Reports — StockFlow",
  description: "Stock valuation, movement history, and exports.",
};

export default function ReportsPage() {
  return (
    <div className="flex flex-col gap-2">
      <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-50">
        Reports
      </h1>
      <p className="text-sm text-slate-500 dark:text-slate-400">
        Valuation, movement history, and CSV/PDF export land here in Phase 9.
      </p>
    </div>
  );
}
