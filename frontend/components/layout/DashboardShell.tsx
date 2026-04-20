import React from "react";

const navItems = [
  { label: "Dashboard", active: true },
  { label: "Tasks", active: false },
  { label: "Imports", active: false },
  { label: "AI Insights", active: false },
  { label: "Reports", active: false },
  { label: "Settings", active: false }
];

function PulseLogo() {
  return (
    <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-primary via-secondary to-accent text-sm font-bold text-white shadow-glow">
      FP
    </div>
  );
}

export function DashboardShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-paper text-ink">
      <aside className="fixed inset-y-0 left-0 z-30 hidden w-72 border-r border-line bg-white/88 backdrop-blur-xl lg:flex lg:flex-col">
        <div className="flex h-16 items-center gap-3 border-b border-line px-5">
          <PulseLogo />
          <div>
            <p className="text-sm font-semibold tracking-tight">FocusPulse</p>
            <p className="text-xs text-muted">Productivity analytics</p>
          </div>
        </div>

        <nav className="flex-1 space-y-6 overflow-y-auto px-3 py-5" aria-label="Dashboard navigation">
          <div>
            <p className="px-3 text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">Workspace</p>
            <div className="mt-3 space-y-1">
              {navItems.map((item) => (
                <a
                  aria-current={item.active ? "page" : undefined}
                  className={`focus-ring flex items-center justify-between rounded-xl px-3 py-2.5 text-sm font-medium transition-colors ${
                    item.active
                      ? "bg-gradient-to-r from-primary/10 to-secondary/10 text-primary"
                      : "text-muted hover:bg-slate-100 hover:text-ink"
                  }`}
                  href="#"
                  key={item.label}
                >
                  <span>{item.label}</span>
                  {item.active ? <span className="h-2 w-2 rounded-full bg-accent" aria-hidden="true" /> : null}
                </a>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-indigo-100 bg-gradient-to-br from-indigo-50 via-white to-cyan-50 p-4 shadow-card">
            <p className="text-sm font-semibold text-ink">AI analysis ready</p>
            <p className="mt-2 text-xs leading-5 text-muted">
              New weekly productivity recommendations are prepared for review.
            </p>
            <button className="focus-ring mt-4 rounded-lg bg-gradient-to-r from-primary to-secondary px-3 py-2 text-xs font-semibold text-white shadow-glow transition hover:brightness-105">
              Review insights
            </button>
          </div>
        </nav>

        <div className="border-t border-line p-4">
          <div className="rounded-2xl border border-line bg-slate-50 p-3">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-muted">Plan</p>
            <div className="mt-2 flex items-center justify-between">
              <span className="text-sm font-semibold">Operations Pro</span>
              <span className="rounded-full bg-success/10 px-2 py-1 text-xs font-semibold text-success">Live</span>
            </div>
          </div>
        </div>
      </aside>

      <div className="lg:pl-72">
        <header className="sticky top-0 z-20 border-b border-line bg-white/78 backdrop-blur-xl">
          <div className="flex h-16 items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
            <div className="flex items-center gap-3 lg:hidden">
              <PulseLogo />
              <span className="text-sm font-semibold">FocusPulse</span>
            </div>
            <div className="hidden min-w-0 items-center gap-2 text-sm text-muted lg:flex">
              <span>Workspace</span>
              <span aria-hidden="true">/</span>
              <span className="font-semibold text-ink">Analytics dashboard</span>
            </div>
            <div className="flex flex-1 items-center justify-end gap-3">
              <div className="hidden w-full max-w-sm items-center rounded-xl border border-line bg-slate-50 px-3 py-2 text-sm text-muted shadow-sm sm:flex">
                <span aria-hidden="true" className="mr-2 text-primary">
                  Search
                </span>
                <span className="truncate">tasks, categories, imports...</span>
              </div>
              <button className="focus-ring rounded-xl border border-line bg-white px-3 py-2 text-sm font-semibold text-ink shadow-sm transition hover:border-primary/40 hover:text-primary">
                Export
              </button>
            </div>
          </div>
        </header>

        <main className="min-h-[calc(100vh-4rem)]">
          <div className="mx-auto flex max-w-[1500px] flex-col gap-6 px-4 py-6 sm:px-6 lg:px-8">{children}</div>
        </main>
      </div>
    </div>
  );
}
