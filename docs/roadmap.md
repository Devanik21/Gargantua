# INTERSTELLAR · Documentation Roadmap

> Static intent declaration for the self-maintaining docs system.
> Last confirmed: 2026-06-13 14:15 UTC

---

## What This System Does

The `interstellar_docs.yml` GitHub Actions workflow maintains a live
documentation layer for the INTERSTELLAR — Gargantua Science Platform.

It runs on a pseudo-random schedule (8 check windows per day, one active
per day, chosen deterministically by date) so commit times feel organic,
not robotic. It can also be triggered manually via `workflow_dispatch`.

---

## Rules (Hard Constraints)

- **Read-only access** to all `.py` files and `README.md`
- **Write access** only within `docs/` — never touches source code
- **Commit only on real diffs** — if docs content didn't change, no commit
- **No fake activity** — changelog only records actual `.py` / README changes
- **7-day history TTL** — old snapshots are auto-deleted to prevent bloat
- **Idempotent** — running twice on the same day is safe

---

## Files Managed

| File | Update Condition |
|------|-----------------|
| `docs/feature-map.md` | Any tracked file changes |
| `docs/system-status.md` | Every successful run |
| `docs/index.md` | First run or structural change |
| `docs/roadmap.md` | First run only (static) |
| `docs/changelog.md` | `.py` or `README.md` changes only |
| `docs/generated/history/YYYY-MM-DD.md` | Repo changed or first run |

---

## What It Does NOT Do

- Generate AI content or summaries
- Modify `.py` files or `README.md`
- Write anything outside `docs/`
- Commit when nothing changed
- Guarantee a daily commit (only commits on real diffs)
- Inflate the contribution graph with fake activity

---

*"Mankind was born on Earth. It was never meant to die here." — Cooper, 2067*
