# INTERSTELLAR · Documentation Roadmap

> Static intent declaration for the self-maintaining docs system.
> Last confirmed: 2026-06-13 14:40 UTC

---

## What This System Does

The `interstellar_docs.yml` GitHub Actions workflow maintains a live
documentation layer for the INTERSTELLAR — Gargantua Science Platform.

It runs twice daily on a fixed UTC schedule:
- **Slot A** — 06:17 UTC (~11:47 IST) — morning run
- **Slot B** — 18:43 UTC (~00:13 IST) — evening run

Both slots always commit. The `docs/mission-log.md` file contains a
per-second UTC timestamp and cumulative run counter, guaranteeing a real
diff on every execution. This keeps the repository active forever and
prevents GitHub's 60-day inactivity auto-pause.

---

## Hard Rules

- **Read-only** access to all `.py` files and `README.md`
- **Write access** only inside `docs/` and `.github/keepalive/` — source never touched
- **No fake content** — every file contains real extracted data
- **Changelog** updated only on actual `.py` / README file changes
- **30-day history TTL** — rolling window of daily snapshots, auto-purged
- **Idempotent** — running a third time on the same day is safe
- **Concurrency-safe** — concurrent runs are serialised; no race conditions

---

## Files Managed

| File | Update Condition |
|------|-----------------|
| `docs/mission-log.md` | **Every run** (per-second timestamp) |
| `docs/feature-map.md` | Any tracked file changes |
| `docs/system-status.md` | Any tracked file changes |
| `docs/index.md` | First run or structural change |
| `docs/roadmap.md` | First run only (static) |
| `docs/changelog.md` | `.py` or `README.md` changes only |
| `docs/generated/history/YYYY-MM-DD.md` | **Every run** (30-day rolling window) |
| `.github/keepalive/active.md` | **Every run** (inactivity-proof sentinel) |

---

## What It Does NOT Do

- Generate AI content or invented summaries
- Modify `.py` files or `README.md`
- Write anything outside `docs/` or `.github/keepalive/`
- Create meaningless / padded commits
- Skip a commit (no early-exit; mission-log + sentinel always differ)

---

*"Mankind was born on Earth. It was never meant to die here." — Cooper, 2067*
