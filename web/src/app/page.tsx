import { Suspense } from "react";

import { getHealth } from "@/lib/api";

export default function Home() {
  return (
    <main className="mx-auto flex w-full max-w-xl flex-1 flex-col gap-6 px-4 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">Review site</h1>
      <p className="text-zinc-600 dark:text-zinc-400">
        Log, rate, and review the games you play.
      </p>
      <Suspense fallback={<p className="text-sm text-zinc-500">Checking API…</p>}>
        <ApiStatus />
      </Suspense>
    </main>
  );
}

async function ApiStatus() {
  const health = await getHealth();

  if (!health) {
    return <p className="text-sm text-red-600">API: unreachable</p>;
  }

  return (
    <ul className="text-sm">
      <li>API: {health.status}</li>
      <li>Postgres: {health.postgres}</li>
      <li>Redis: {health.redis}</li>
    </ul>
  );
}
