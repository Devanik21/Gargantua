# INTERSTELLAR · Documentation Bot — Roadmap & Rules

> Static intent declaration. Written once; updated only on force-refresh.
> Bot initialised: `2026-06-14`

---

## Purpose

The `interstellar_docs.yml` GitHub Actions workflow is a self-maintaining
documentation bot for the **INTERSTELLAR — Gargantua Science Platform**.

It reads all `.py` files in the repository root and `README.md` on every
run, produces genuinely useful documentation in `docs/`, and commits only
real content — never noise.

---

## Schedule

Three cron slots fire every calendar day (UTC):

| Slot | Time (UTC) | Time (IST) | Label |
|------|-----------|------------|-------|
| A | 05:17 | 10:47 | morning |
| B | 13:29 | 18:59 | afternoon |
| C | 21:43 | 03:13 +1 | night |

All three always run. This guarantees **2–3 commits per day** regardless
of whether source files changed, which prevents GitHub's 60-day inactivity
auto-pause from ever triggering.

A manual `workflow_dispatch` trigger (with optional `force_refresh`) is
also available for spot-checks and forced resyncs.

---

## Files Managed

| File | Condition |
|------|-----------|
| `docs/mission-log.md` | **Always written** (timestamp ensures real diff) |
| `docs/feature-map.md` | Written when source changes |
| `docs/system-status.md` | Written when source changes |
| `docs/code-intelligence.md` | Written when source changes |
| `docs/index.md` | Written when source changes |
| `docs/roadmap.md` | Written on first run only |
| `docs/changelog.md` | Written when `.py` or `README.md` changes |
| `docs/generated/history/*.md` | **Always written** (one file per slot) |

---

## Hard Rules

1. **Source is read-only.** No `.py` file or `README.md` is ever written.
2. **docs/ is the only playground.** Nothing outside `docs/` is staged.
3. **No fake content.** Every field in every doc reflects real repo state.
4. **Future-proof.** New `.py` files added to root are auto-discovered.
5. **Self-cleaning.** History files older than 7 days are auto-deleted.
6. **Idempotent.** Running twice in the same slot is safe.
7. **Zero pip deps.** Pure Python stdlib — no install step ever fails.

---

## What It Does NOT Do

- Generate AI-written summaries or fictional content
- Modify, rename, or delete any source file
- Write outside `docs/`
- Inflate the graph with empty commits
- Depend on any external API or secret

---

*"Do not go gentle into that good night." — Dylan Thomas (and TARS)*
