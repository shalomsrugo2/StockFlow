import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-24 text-center">
      <h1 className="text-lg font-semibold text-slate-900 dark:text-slate-50">
        Page not found
      </h1>
      <p className="max-w-sm text-sm text-slate-500 dark:text-slate-400">
        The page you&apos;re looking for doesn&apos;t exist or has moved.
      </p>
      <Link href="/dashboard" className="text-sm font-medium text-accent">
        Back to dashboard
      </Link>
    </div>
  );
}
