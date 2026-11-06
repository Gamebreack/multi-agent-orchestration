# Flow map — from clone to a verified commit

How MAO works end to end: you clone the repo and ask your agent to read and follow `core/skills/mao-setup/SKILL.md` (A); from then on every task you give the agent is planned, delegated to role agents, checked per the verification ladder, and committed only when you ask (B). Pushing stays with you. This is the largest flow in the repo; uninstall is drawn as a side path, and the repo's own ICM work stages (`stages/`; `starter/` is the template for other projects) are a separate flow not drawn here.

Renders on GitHub and in any Markdown viewer with Mermaid support.

> **Status:** Every step is described in the sources; nothing is missing. MAO is instructions, not code: each step is carried out by your agent following them. Tool limits are hard only where your harness can enforce them; elsewhere they are prompt-only, and `mao-setup` says which in its plan.
> Lines: solid = exists · red dashed or red band = missing · dotted = optional or read-only · "no code yet" (or "not described") box = missing stage · grey = outside the target · light grey dashed box = side path

## 1. What happens

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"system-ui, -apple-system, Segoe UI, sans-serif","fontSize":"15px","primaryTextColor":"#1b221e","lineColor":"#8a968f","clusterBkg":"transparent","clusterBorder":"#b7c0ba","titleColor":"#5d6962","edgeLabelBackground":"#ffffff"},"flowchart":{"curve":"basis","nodeSpacing":22,"rankSpacing":30,"padding":14,"htmlLabels":true,"subGraphTitleMargin":{"top":6,"bottom":14}}}}%%
flowchart TD
    U["<b>You</b><br/>clone, point agent at mao-setup"]
    HD["<b>Harness docs</b><br/>live docs or --help"]
    REQ["<b>Your task</b><br/>any request to the agent"]
    PUSH["<b>Push</b><br/>you decide · agent pushes only if asked"]
    UN["<b>Uninstall</b><br/>you ask · approve, then reverse manifest"]
    TRIV["<b>Trivial edit</b><br/>one-line, low-risk · done directly"]
    FB["<b>No subagents</b><br/>main agent works at role rigor"]

    subgraph F1["Phase 1 · Install"]
        S1["<b>Detect harness</b><br/>reads its live docs"]
        S2["<b>Plan the links</b><br/>instructions, skills, roles, retirements"]
        S3["<b>Optional dependencies</b><br/>each asked y/N"]
        S4["<b>Approve the plan</b><br/>nothing written before · dry-run stops"]
        S5["<b>Apply and record</b><br/>backups first, manifest per action"]
        S6["<b>Smoke test</b><br/>check mao-reviewer's tools vs plan"]
    end

    subgraph F2["Phase 2 · Plan (every task)"]
        P1["<b>Main agent plans</b><br/>reads code and context, picks approach"]
    end

    subgraph F3["Phase 3 · Delegate"]
        D1["<b>Pick role and tier</b><br/>cheapest that works · escalate on failure"]
        D2["<b>Role agents work</b><br/>≤3 implementers at once, own checks"]
    end

    subgraph F4["Phase 4 · Verify and commit"]
        V1["<b>Fresh-context check</b><br/>ladder: verifier, reviewer, panel"]
        C1["<b>Commit on request</b><br/>pre-commit hooks run, never skipped"]
    end

    U -->|"read and follow"| S1
    %% 1: read-only
    HD -.->|"read"| S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 -->|"approved"| S5
    S5 --> S6
    S6 -->|"installed"| P1
    REQ -->|"task"| P1
    %% 9: side path
    P1 -.->|"trivial"| TRIV
    P1 -->|"delegate"| D1
    %% 11: side path
    P1 -.->|"no subagents"| FB
    D1 -->|"brief"| D2
    D2 <-->|"report, findings"| V1
    V1 -->|"you ask"| C1
    C1 --> PUSH
    %% 16: side path
    S5 -.->|"manifest"| UN
    %% 17: side path
    TRIV -.->|"untracked: own check"| C1
    %% 18: side path
    FB -.->|"not independent"| C1
    %% 19: side path
    TRIV -.->|"tracked item"| V1

    classDef ext fill:#e7eae8,stroke:#8a968f,color:#1b221e
    classDef p1 fill:#dbe8f6,stroke:#4a7fb5,color:#1b221e
    classDef p2 fill:#fbefd2,stroke:#c3962c,color:#1b221e
    classDef p3 fill:#d8eee2,stroke:#3f8f68,color:#1b221e
    classDef p4 fill:#e7def4,stroke:#7a5aa6,color:#1b221e
    classDef side fill:#f5f6f5,stroke:#a9b4ad,color:#5d6962,stroke-dasharray:4 3
    class U,HD,REQ,PUSH ext
    class S1,S2,S3,S4,S5,S6 p1
    class P1 p2
    class D1,D2 p3
    class V1,C1 p4
    class UN,TRIV,FB side
    linkStyle 1,9,11,16,17,18,19 stroke:#8a968f,stroke-width:1.5px,stroke-dasharray:2 3
```

| Phase | In one line |
|---|---|
| Install | Once per harness; re-run to update. Your agent reads its harness's live docs, plans every link and file, asks y/N per optional dependency, writes nothing until you approve, backs up and records each action, then smoke-tests one role agent. A failed check is reported as FAILURE, never passed; any plan change needs approval again. Uninstall (on request) shows a reverse plan of this harness's recorded actions and undoes them after approval; items another harness still uses are kept; anything altered since install is kept by default; retired items are not restored unless you opt in. |
| Plan | For each task the main agent reads the code and project context and chooses an approach. A one-line change it may do itself. Without subagent support it does the role work itself and never presents its own check as independent. |
| Delegate | It briefs the cheapest role that can do the work reliably (`mao-hard-implementer` only for hard, high-risk or failed work); implementers edit and run their own checks; every worker reports and never spawns workers. With no `mao-<role>` subagent installed, a generic subagent reads the role's charter. `mao-documenter` runs only when docs are requested or made inaccurate, once behavior is settled. |
| Verify and commit | Checks follow the verification ladder: a trivial, low-risk edit outside a tracked work item gets the implementer's own check; every other change is checked in a fresh context, never by the author — a verifier for any other change or any tracked item, plus a reviewer when it is significant or risky, plus an independent panel before a version is tagged; where rungs overlap, the highest applies, and a change to the ladder itself is checked under the base branch's ladder, at the significant rung or higher. Findings go back to the implementing role. The agent commits only when you ask, after the repo's pre-commit hooks pass (failures fixed, never bypassed); pushing is yours. |

## 2. Who talks to whom

You talk only to your agent. It reads MAO, links it into the harness, records what it did locally, and delegates to role agents that work in your project. Colors here only tell who is who.

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"system-ui, -apple-system, Segoe UI, sans-serif","fontSize":"15px","primaryTextColor":"#1b221e","lineColor":"#8a968f","edgeLabelBackground":"#ffffff"},"flowchart":{"curve":"basis","nodeSpacing":36,"rankSpacing":44,"padding":14,"htmlLabels":true}}}%%
flowchart TD
    YOU["<b>You</b><br/>requests and approvals"]
    AG["<b>Your agent harness</b><br/>runs the main agent"]
    MAO["<b>MAO repo</b><br/>core/AGENTS.md + mao-* skills"]
    CFG[("<b>Local MAO state</b><br/>~/.config/mao manifest, backups")]
    UP["<b>Optional dependencies</b><br/>OpenSpec, verify, megaplan, flow-map, …"]
    SUB["<b>Role agents</b><br/>mao-* subagents in the harness"]
    PRJ["<b>Your project</b><br/>code, tests, git"]

    YOU -->|"asks, approves"| AG
    %% 1: read-only
    AG -.->|"reads, links"| MAO
    AG -->|"records"| CFG
    %% 3: optional
    AG -.->|"installs if y"| UP
    AG -->|"delegates"| SUB
    SUB -->|"edits, tests"| PRJ
    AG -->|"commits"| PRJ
    %% 7: read-only
    SUB -.->|"reads charter"| MAO

    classDef ext fill:#e7eae8,stroke:#8a968f,color:#1b221e
    classDef front fill:#ffffff,stroke:#3d4a43,color:#1b221e,stroke-width:1.5px
    classDef ours fill:#ffffff,stroke:#1b221e,color:#1b221e,stroke-width:2px
    classDef db fill:#ffffff,stroke:#8a968f,color:#1b221e
    class AG,UP,SUB,PRJ ext
    class YOU front
    class MAO ours
    class CFG db
    linkStyle 1,3,7 stroke:#8a968f,stroke-width:1.5px,stroke-dasharray:2 3
```

## 3. The life of one task

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"system-ui, -apple-system, Segoe UI, sans-serif","fontSize":"15px","actorBkg":"#e7eae8","actorBorder":"#8a968f","actorTextColor":"#1b221e","actorLineColor":"#c3cbc6","signalColor":"#5d6962","signalTextColor":"#1b221e","sequenceNumberColor":"#ffffff","noteBkgColor":"#f1f3f1","noteBorderColor":"#b7c0ba","noteTextColor":"#1b221e"},"sequence":{"mirrorActors":false,"messageMargin":24,"boxMargin":8,"actorMargin":40,"messageFontSize":15,"actorFontSize":15,"noteFontSize":14}}}%%
sequenceDiagram
    autonumber
    participant YOU as You
    participant MA as Main agent
    participant W as Implementer or mechanical
    participant CK as Verifier or reviewer
    participant PRJ as Your project
    YOU->>MA: asks for a change
    MA->>PRJ: reads code and conventions
    Note over MA: picks the cheapest capable role
    MA->>W: self-contained brief
    W->>PRJ: edits, runs its own checks
    W-->>MA: files changed, commands, results
    MA->>CK: fresh-context check
    CK-->>MA: evidence or ranked findings
    opt findings
        MA->>W: findings to fix, then recheck
    end
    YOU->>MA: asks for a commit
    MA->>PRJ: runs pre-commit hooks, commits
    Note over YOU,PRJ: Push stays with you
```

## Where it lives

| Phase | Path |
|---|---|
| Install | `core/skills/mao-setup/SKILL.md`, `core/skills/mao-setup/manifest.md` |
| Plan | `core/AGENTS.md` (Main agent, Roles and tiers) |
| Delegate | `core/AGENTS.md` (Delegation), `core/skills/mao-<role>/SKILL.md` |
| Verify and commit | `core/AGENTS.md` (Delegation step 8, Committing), `docs/policies.md` (Verification ladder) |

Glossary: [docs/megaplan/glossary.md](docs/megaplan/glossary.md).

When the flow changes, the map changes in the same PR. To update, see what changed since the commit below.

Updated 2026-11-05 · multi-agent-orchestration docs/b12-ladder-changelog babaabc
