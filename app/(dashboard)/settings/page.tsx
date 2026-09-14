import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Settings — StockFlow",
  description: "Company profile, users, and roles.",
};

export default function SettingsPage() {
  return (
    <div className="flex flex-col gap-2">
      <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-50">
        Settings
      </h1>
      <p className="text-sm text-slate-500 dark:text-slate-400">
        Auth, roles, and account settings land here in Phase 2.
      </p>
    </div>
  );
}
