# Manifest and uninstall

Reference for `mao-setup`. Manifest: `~/.config/mao/installed.json`. Append; never rewrite
history; keep every harness's actions.

```json
{
  "version": 1,
  "repo": "<absolute real path of the repo at install time>",
  "updated": "<ISO 8601>",
  "actions": [
    {
      "type": "link | write | edit | run | clone | retire",
      "path": "<absolute path affected>",
      "target": "<link target, for link>",
      "backup": "<backup path of the replaced original, or null>",
      "sha256": "<hash of written content, for write/edit>",
      "source": "<repo git short sha the content came from, for generated files>",
      "harness": "<harness that created it>",
      "dependents": ["<every harness relying on it>"],
      "status": "applied | undone",
      "undo": "<how to reverse: remove link, restore backup, npm rm -g <pkg>, ...>",
      "time": "<ISO 8601>"
    }
  ]
}
```

Action names are the same in the plan, the manifest and uninstall. `run` covers package
installs and `npx skills add`; record what changed so it can be undone.

## Shared items

Skill links in `~/.agents/skills`, npm packages and vendor clones can serve several
harnesses. When a later harness finds such an item already correct, append the harness to that
action's `dependents`; status stays `applied`. Never create a duplicate action.

## Uninstall

1. Read the manifest. Missing or empty: report nothing to reverse and stop.
2. Scope: default is the current harness only; `--all` (explicit) covers every harness.
   For each action in scope, an action is reversible only if no harness outside the scope
   remains in `dependents`; otherwise it is kept, naming the dependents.
3. Build the reverse plan, newest first, and show it in full (dry-run), computing which
   dependents would be removed and which actions would be reversed; write nothing, and
   change no `dependents` or `status` until the user approves. Before each undo,
   check current state: a link or file that no longer matches what was recorded (target,
   `sha256`) was altered since install; flag it and default to leaving it.
4. After explicit approval, update `dependents` and then remove links and written files, restore backups, run the
   recorded `undo` for packages and clones. Only reverse what the manifest says MAO
   installed; never remove something that existed before.
5. `retire` actions are not restored unless the user explicitly opts in.
6. Set `status` to `undone` (keep the file) and report what was reversed and what was left.
