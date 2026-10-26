# End-of-day sync (optional workflow)

Turn one day of work into a small batch of brain records the user approves before anything
is sent. Writes to the brain only. Reply in the user's language. Follow the parent skill for
tool behavior (search before create, concurrency fields, idempotency).

Optional arguments: a date (default today) and/or project names to limit scope.

## 1. Collect

Gather what happened that day from whatever the harness and repos make available: session
transcripts or history for the day, and the user's commits. Keep user and agent messages,
files edited and commits; leave out tool output and reasoning. Summarize large sources
through read-only subagents that return candidates only and write nothing; the approval gate
below applies to them too.

In parallel, fetch the brain's context snapshot, projects, task lists, people, pending
reminders, active goals and current priorities, so records can link to existing entities and
be deduplicated.

## 2. Distill: what is worth a record

Test: would a future agent or the user make a better call next week knowing this, and is it
written down nowhere else?

| Found in the day | Record |
|---|---|
| A choice with its reason (and dropped alternatives) | decision |
| A pattern or convention created or adopted | memory (pattern) |
| Understanding reached: how a system behaves, a domain rule, a root cause, a gotcha | memory (understanding) |
| How the user wants to work, or a correction they gave | memory (preference) |
| An open personal or cross-cutting commitment not tracked elsewhere | task |
| A person relevant to the work who is not in the brain, or a changed role | person create or update |
| A meeting, or a message that asked for or decided something | activity |
| A dated follow-up | reminder with a concrete time |
| A goal that moved, or priorities the user explicitly set | goal or priority update |

Leave out: anything already recorded in the repo, git or a tracker; dead-end debugging;
temporary branch or PR state; secrets and customers' personal data; guesses (only what the
user stated or what was verified); sensitive personal data about people; messages with no
consequence.

Each record must stand alone: name the system, say what is true or decided, say why, in 1-5
sentences. Prefer fewer, denser records; a typical day yields 3-12. Merge records on the same
subject.

## 3. Dedupe, then propose

Check earlier runs for the same date first (a local ledger of handled items, and a search of
the brain for that day's tag), then search the brain for each remaining candidate. Mark each:
- **new**
- **update #id**: an existing record covers it but is stale (read it first for version and
  hash; decisions are superseded, not edited)
- **drop**: already covered; list it in one line and do not propose it

Do not re-propose what the user rejected earlier unless something new came up.

Show one numbered batch, one small table per project or area (number, type, plain gist), a
bold line with the item count and the already-synced count, and a short "Not sent" list.
State in the gist what was guessed or assumed. A reminder's time must be concrete; mark an
assumed one. End with: `Reply "ok", "drop 2,5", or "edit 3: <text>".` Write nothing until
the user approves.

## 4. Send

Write only approved items, in parallel where independent, except new people first so their
IDs can link the rest.
- Derive each idempotency key deterministically from the date, the tool and a short hash of
  the canonical payload, so a retry reuses it and a different item gets a new one.
- Use full timestamps with a UTC offset where the server asks for them. If the server
  rejects client-supplied "captured/decided at" timestamps, omit them and put the date in the
  text and a day tag instead.
- Tag records with the repo name, one to three topical tags and a day tag.
- Append each confirmed write (and each rejected item) to a local ledger; never log a failed
  write. Save failed payloads with their keys and offer to retry them unchanged next run.
- Prefer direct writes over server-side ingestion, so the user approves the exact text that
  is stored.

Report one line per item: number and record ID, or the error.
