# Suzerain

> *"The suzerain rules even where there are other kings. There is no territory outside his claim."*

**You are the suzerain. The AI executes, but you rule.**

Suzerain analyzes how you govern AI coding assistants—your patterns of trust, rejection, and deliberation—and classifies your style into historical archetypes.

## Quick Start

```bash
pip install suzerain
suzerain analyze
```

## What You Get

```
  ╔═══════════════════════════════════════════════════════╗
  ║                      SUZERAIN                         ║
  ║                                                       ║
  ║   "The suzerain rules even where there are other      ║
  ║    kings. There is no territory outside his claim."   ║
  ╚═══════════════════════════════════════════════════════╝

  Your recent pattern: STRATEGIST
  Empirical cluster: Casual (Cautious)

  ┌─ YOUR GOVERNANCE STYLE ───────────────────────────────┐
  │ The Discrimination Game
  │
  │ You rule differently depending on the stakes. Safe
  │ operations flow through unchallenged; risky operations
  │ face scrutiny. Same AI, different trust levels based
  │ on consequences.
  └────────────────────────────────────────────────────────┘

  ┌─ YOUR BOTTLENECK ────────────────────────────────────┐
  │ Decision overhead on edge cases
  │
  │ Your selective trust is efficient for clear-cut cases.
  │ The bottleneck is ambiguous commands—things that might
  │ be risky. You may over-deliberate on medium-risk
  │ operations.
  └────────────────────────────────────────────────────────┘

  ┌─ KEY METRICS (Karpathy-approved) ────────────────────┐
  │ Bash acceptance:      54% ← THE discriminator
  │ Snap judgments:       62% (decisions < 500ms)
  │ Risk delta:           +33% (safe vs risky trust gap)
  │ Sophistication:       0.50
  │ Caution:              0.80
  └────────────────────────────────────────────────────────┘

  ┌─ ONE THING TO TRY ───────────────────────────────────┐
  │ Try the Task tool for one complex operation. Agents
  │ can do the risky exploration while you maintain
  │ oversight.
  └────────────────────────────────────────────────────────┘

  Based on 70 sessions, 6,247 tool calls, 26 days
  ● Higher confidence: pattern appears stable

  ─────────────────────────────────────────────────────────
  You are the suzerain. The AI executes, but you rule.
  These patterns describe how you exercise your claim—
  not who you are. The game changes when you do.
```

## The Six Archetypes

| Archetype | Governance Style | Bottleneck | Historical Parallel |
|-----------|------------------|------------|---------------------|
| **Delegator** | Accept everything, fast | Errors surface downstream | Mongol Horde |
| **Autocrat** | Review all, approve all | Review time without filtering | Roman Emperor |
| **Strategist** | Selective by risk | Decision overhead on edge cases | Napoleon |
| **Deliberator** | Slow, thorough | Decision latency on everything | Athenian Assembly |
| **Council** | Orchestrates agents | Coordination overhead | Venetian Republic |
| **Constitutionalist** | Consistent patterns | Rule rigidity | Constitutional systems |

## How It Works

Suzerain parses your Claude Code logs (`~/.claude/projects/`) and extracts:
- Tool acceptance/rejection rates
- Decision timing (snap judgments vs deliberation)
- Tool diversity and sophistication signals

**Key finding:** Bash acceptance is THE discriminating feature. All other tools have ~100% acceptance rate—governance happens at the Bash prompt.

## Commands

```bash
suzerain analyze            # Analyze your governance style
suzerain analyze --verbose  # Full metrics breakdown
suzerain analyze --export   # Export to JSON
suzerain share --preview    # See what would be shared
suzerain share --confirm    # Share anonymized metrics (opt-in)
```

## Privacy

- **Local-first:** All analysis runs on your machine
- **Opt-in only:** Nothing shared without explicit consent
- **Minimal data:** Only aggregate metrics, never prompts or code
- **Transparent:** Preview exactly what would be shared before opting in

## Epistemic Status

This tool is **hypothesis-generating, not validated**:
- Based on n=1 real user + 11 simulated personas
- Thresholds are heuristic, not empirically derived
- Patterns describe recent behavior, not personality
- We need more data—your participation helps

See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for honest disclosure.

## Contributing

We need diverse user data to validate the archetypes:

```bash
suzerain share --preview  # See what would be shared
suzerain share --confirm  # Help improve the research
```

## License

MIT

---

*"What kind of ruler are you today?"*
