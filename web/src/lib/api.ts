// Server-side base URL for the FastAPI backend. Not prefixed with NEXT_PUBLIC_,
// so it is never sent to the browser.
export const API_URL = process.env.API_URL ?? "http://localhost:8001";

export type Health = {
  status: "ok" | "degraded";
  postgres: "ok" | "down";
  redis: "ok" | "down";
};

export async function getHealth(): Promise<Health | null> {
  try {
    const res = await fetch(`${API_URL}/health`);
    return (await res.json()) as Health;
  } catch {
    // API not running or unreachable.
    return null;
  }
}
