import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Catalog — StockFlow",
  description: "Browse and manage products, variants, and categories.",
};

export default function CatalogPage() {
  return (
    <div className="flex flex-col gap-2">
      <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-50">
        Catalog
      </h1>
      <p className="text-sm text-slate-500 dark:text-slate-400">
        Product, variant, and category CRUD lands here in Phase 4.
      </p>
    </div>
  );
}
