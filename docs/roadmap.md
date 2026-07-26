# INTERSTELLAR · Documentation Bot — Roadmap & Rules

> Static intent declaration. Written once; updated only on force-refresh.
> Bot initialised: `2026-07-26`

---

## Purpose

The `interstellar_docs.yml` GitHub Actions workflow is a self-maintaining
documentation bot for the **INTERSTELLAR — Gargantua Science Platform**.

It reads all `.py` files in the repository root and `README.md` on every
run, produces genuinely useful documentation in `docs/`, and commits only
real content — never noise.

---

## Schedule

Four cron slots fire every calendar day (UTC):

| Slot | Time (UTC) | Time (IST) | Label |
|------|-----------|------------|-------|
| A | 05:17 | 10:47 | morning |
| B | 13:29 | 18:59 | afternoon |
| D | 17:36 | 23:06 | evening |
| C | 21:43 | 03:13 +1 | night |

Each day the bot draws a random commit quota of **1–4** and stores it in
`.bot/state.json` (persisted across runs via GitHub Actions cache). Slots
beyond that day's quota exit before writing or committing anything, so
the real commit count varies day to day between 1 and 4. Since at least
one commit always lands, this still prevents GitHub's 60-day inactivity
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
