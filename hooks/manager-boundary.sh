#!/usr/bin/env bash
# manager-boundary.sh — PreToolUse hook enforcing "THE MANAGER NEVER IMPLEMENTS".
#
# Two installation points, same script:
#   --global  (in ~/.claude/settings.json, matcher "*"): acts ONLY when the hook input
#             identifies the acting agent as `manager` (agent_type == "manager").
#             Absent agent_type = an ordinary session or the main thread -> allow.
#   --scoped  (in ~/.claude/agents/manager.md frontmatter hooks): the hook only exists
#             while the manager agent runs, so absent agent_type == the manager itself
#             running as the main session (`claude --agent manager`) -> enforce.
#             Child agents (agent_type set to something else) -> allow.
#
# Enforcement is an ALLOW-LIST: only inspection / coordination / delegation tools pass;
# everything else (Edit, Write, NotebookEdit, Bash, PowerShell, Monitor, Workflow, worktree
# tools, unknown or renamed tools, any MCP server not explicitly allowed) is denied with a useful
# reason. Agent spawns are limited to the declared roles. Structured hook JSON is used; no
# fragile text matching on prompts.
#
# Fail-safe: if the input cannot be parsed we never deny an unidentified session
# (--global), and we deny in --scoped mode (fail closed for the manager). Set
# MANAGER_BOUNDARY_LOG=/path to append every decision (debugging / validation).
set -u
mode="${1:---global}"
input=$(cat 2>/dev/null || true)

deny() {
  local reason="$1"
  if command -v jq >/dev/null 2>&1; then
    jq -n --arg r "$reason" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
    exit 0
  fi
  printf '%s\n' "$reason" >&2
  exit 2
}

log() {
  [ -n "${MANAGER_BOUNDARY_LOG:-}" ] || return 0
  printf '%s\t%s\t%s\t%s\t%s\n' "$(date +%H:%M:%S 2>/dev/null || echo -)" "$mode" "${agent_type:-<main>}" "${tool:-?}" "$1" >>"$MANAGER_BOUNDARY_LOG" 2>/dev/null || true
}

agent_type=""; tool=""; subagent=""
if command -v jq >/dev/null 2>&1; then
  agent_type=$(printf '%s' "$input" | jq -r '.agent_type // empty' 2>/dev/null || true)
  tool=$(printf '%s' "$input" | jq -r '.tool_name // empty' 2>/dev/null || true)
  subagent=$(printf '%s' "$input" | jq -r '.tool_input.subagent_type // empty' 2>/dev/null || true)
else
  # Degraded parsing without jq: pure bash (no external tools), fail CLOSED for the
  # manager. Any "agent_type":"manager" anywhere in the payload counts as the manager; if
  # several distinct tool_name / subagent_type values appear (nested spoof) the value is
  # treated as unparsed, which the manager branch denies.
  if [[ "$input" =~ \"agent_type\"[[:space:]]*:[[:space:]]*\"manager\" ]]; then
    agent_type=manager
  elif [[ "$input" =~ \"agent_type\"[[:space:]]*:[[:space:]]*\"([^\"]*)\" ]]; then
    agent_type="${BASH_REMATCH[1]}"
  fi
  uniq_field() {  # $1 = key; prints the single distinct value, or nothing if 0 or >1 distinct
    local rest="$input" v="" found=""
    while [[ "$rest" =~ \"$1\"[[:space:]]*:[[:space:]]*\"([^\"]*)\"(.*)$ ]]; do
      v="${BASH_REMATCH[1]}"; rest="${BASH_REMATCH[2]}"
      if [ -z "$found" ]; then found="$v"; elif [ "$found" != "$v" ]; then return 0; fi
    done
    printf '%s' "$found"
  }
  tool=$(uniq_field tool_name)
  subagent=$(uniq_field subagent_type)
fi

# ---- Decide whether the acting agent is the manager --------------------------------
is_manager=0
case "$mode" in
  --scoped)
    # Frontmatter hook: exists only while manager runs. Main-thread manager has no
    # agent_type; a manager spawned as a subagent has agent_type=manager.
    if [ -z "$agent_type" ] || [ "$agent_type" = "manager" ]; then is_manager=1; fi
    ;;
  *)
    [ "$agent_type" = "manager" ] && is_manager=1
    ;;
esac

if [ "$is_manager" -eq 0 ]; then log allow-not-manager; exit 0; fi

if [ -z "$tool" ]; then
  # Could not identify the tool. Fail closed for the manager.
  log deny-unparsed
  deny "manager-boundary: could not parse tool call; the Manager is orchestration-only. Delegate this to an appropriate worker."
fi

# ---- Allow-list for the manager -----------------------------------------------------
ALLOWED_AGENTS="explorer mechanical-worker worker hard-worker reviewer verifier"
case "$tool" in
  Read|Grep|Glob|LSP|WebFetch|WebSearch|TodoWrite|TaskOutput|TaskStop|SendMessage|ListAgents|Skill|ToolSearch|AskUserQuestion|EnterPlanMode|ExitPlanMode|ScheduleWakeup|ListMcpResourcesTool|ReadMcpResourceTool|ReadMcpResourceDirTool|PushNotification|SendUserFile|SendFeedback|CronCreate|CronDelete|CronList)
    log allow; exit 0 ;;
  Agent)
    for a in $ALLOWED_AGENTS; do
      [ "$a" = "$subagent" ] && { log "allow-agent:$subagent"; exit 0; }
    done
    log "deny-agent:${subagent:-<none>}"
    deny "manager-boundary: the Manager may only delegate to explorer, mechanical-worker, worker, hard-worker, reviewer or verifier (got subagent_type='${subagent:-<none>}'). Pick the appropriate declared role; do not create ad-hoc agents or forks." ;;
  mcp__*)
    # MCP is an ALLOW-LIST too: only coordination servers the manager is meant to use
    # pass (card updates, long-term memory, inspecting external systems). Every other
    # MCP server — including any future file-editing, git, shell or code-execution
    # server — is denied for the manager.
    # Add a server deliberately as: mcp__<server>__*
    case "$tool" in
      # allow your own servers here, e.g.: mcp__<server>__*) log allow-mcp; exit 0 ;;
      *)
        log deny-mcp
        deny "manager-boundary: MCP tool '$tool' is not on the Manager's coordination allow-list (none by default). If it mutates the repository, delegate to a worker; if it is a new coordination server, add mcp__<server>__* to the hook." ;;
    esac ;;
  Edit|Write|MultiEdit|NotebookEdit|Bash|PowerShell|Monitor|Workflow|EnterWorktree|ExitWorktree|*)
    log deny
    deny "manager-boundary: '$tool' is denied. The Manager is orchestration-only and never implements — not even a one-line change. Delegate this to mechanical-worker / worker / hard-worker (implementation), verifier (commands, tests, builds) or explorer (read-only investigation)." ;;
esac
