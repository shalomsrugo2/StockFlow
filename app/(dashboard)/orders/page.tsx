import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Orders — StockFlow",
  description: "Purchase orders and sales orders.",
};

export default function OrdersPage() {
  return (
    <div className="flex flex-col gap-2">
      <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-50">
        Orders
      </h1>
      <p className="text-sm text-slate-500 dark:text-slate-400">
        Purchase orders land here in Phase 7, sales orders in Phase 8.
      </p>
    </div>
  );
}
