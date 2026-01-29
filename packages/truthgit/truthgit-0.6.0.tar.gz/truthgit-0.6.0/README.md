# TruthGit

<div align="center">

**Consensus tracking for AI-assisted verification.**

[![PyPI](https://img.shields.io/pypi/v/truthgit.svg)](https://pypi.org/project/truthgit/)
[![Tests](https://img.shields.io/badge/tests-309%20passed-brightgreen.svg)](https://github.com/lumensyntax-org/truthgit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

[Website](https://truthgit.com) • [Documentation](https://truthgit.com/docs) • [Discord](https://discord.gg/truthgit)

</div>

---

TruthGit tracks claims and their verification status across multiple AI validators. It provides a structured way to document what different AI systems agree or disagree about, and classifies the *type* of disagreement.

```bash
$ truthgit init
$ truthgit claim "Water boils at 100°C at sea level" --domain physics
$ truthgit verify

[OLLAMA:HERMES3] 95% - Accurate under standard atmospheric pressure
[OLLAMA:NEMOTRON] 94% - True at 1 atm, varies with altitude

✓ PASSED  Consensus: 95%
Verification: a7f3b2c1
```

## What TruthGit Is (and Isn't)

### ✅ What It IS

| Capability | Description |
|------------|-------------|
| **Consensus tracking** | Records what multiple AI validators say about a claim |
| **Disagreement classification** | Distinguishes between logical errors, philosophical mysteries, and knowledge gaps |
| **Audit trail** | Immutable history of verification decisions |
| **Consistency checking** | Detects when AI validators give very different answers |
| **Pattern-based heuristics** | Basic detection of common fallacy patterns and hypothesis types |

### ❌ What It Is NOT

| Misconception | Reality |
|---------------|---------|
| **"Verifies absolute truth"** | It verifies *AI consensus*, not objective truth. If all AIs share the same bias, consensus can be wrong. |
| **"Proves facts"** | Cryptographic proofs verify *data integrity* (the hash matches), not *factual accuracy*. |
| **"Deep semantic analysis"** | Fallacy detection uses regex pattern matching, not NLU. It catches obvious patterns, not subtle reasoning errors. |
| **"Scientific fact-checking"** | It doesn't query scientific databases. For real fact-checking, you need PubMed, Semantic Scholar, etc. |
| **"Prevents AI hallucinations"** | Multiple AIs can hallucinate the same thing if trained on similar data. |

### The Fundamental Limitation

```
LLM A says: "X is true" (90%)
LLM B says: "X is true" (85%)
LLM C says: "X is true" (88%)
→ Consensus: PASSED ✓

But if all LLMs learned from the same biased data,
consensus can be consensus of error.
```

**TruthGit is useful for detecting *inconsistency* between validators, not for verifying *ground truth*.**

---

## When TruthGit Is Useful

### Good Use Cases

1. **Detecting AI uncertainty** — If validators disagree significantly, something is uncertain
2. **Classifying disagreement types** — Is this a factual error or a philosophical question?
3. **Documenting decisions** — Audit trail of what AIs said and when
4. **Flagging obvious issues** — Pattern-based detection of common fallacies
5. **Philosophical domains** — Distinguishing ERROR from MYSTERY is conceptually valuable

### Poor Use Cases

1. **Verifying scientific facts** — Use actual scientific databases instead
2. **High-stakes decisions** — Medical, financial, legal decisions need real verification
3. **Novel information** — AIs can't verify things outside their training data
4. **Replacing human judgment** — TruthGit is a tool, not an oracle

---

## Core Concepts

### Ontological Consensus

Most verification systems ask: "How much agreement?" TruthGit also asks: **"What type of disagreement?"**

| Type | Symbol | Meaning | Action |
|------|--------|---------|--------|
| **PASSED** | ✓ | Validators agree above threshold | Claim recorded as verified |
| **LOGICAL_ERROR** | ✗ | One validator shows fallacy patterns | Flag outlier, recalculate |
| **MYSTERY** | ⚡ | Legitimate philosophical disagreement | Preserve all positions |
| **GAP** | ⏳ | Unfalsifiable or needs external data | Escalate to human |

### Why This Classification Matters

```
Traditional: 60% consensus on "Free will exists" → FAILED ❌
TruthGit:    60% consensus on "Free will exists" → MYSTERY ⚡ (preserved)
```

For philosophical questions, disagreement isn't failure—it's information.

---

## Installation

```bash
# Install TruthGit
pip install truthgit

# For local validation with Ollama (no API keys)
pip install truthgit[local]

# For cloud APIs (optional)
pip install truthgit[cloud]
```

### Local Setup (Recommended)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama3
ollama pull mistral

# Verify setup
truthgit validators --local
```

---

## Quick Start

```bash
# Initialize a repository
truthgit init

# Create claims
truthgit claim "The Earth orbits the Sun" --domain astronomy
truthgit claim "Python was created by Guido van Rossum" --domain programming

# Verify with local AI consensus
truthgit verify --local

# View history
truthgit log
```

---

## Commands

| Command | Description |
|---------|-------------|
| `truthgit init` | Initialize a new repository |
| `truthgit claim "..." --domain x` | Create a claim to verify |
| `truthgit verify [--local]` | Verify with ontological consensus |
| `truthgit verify --simple` | Verify with threshold only (no classification) |
| `truthgit status` | Show repository status |
| `truthgit log` | Show verification history |
| `truthgit validators` | Show available validators |

---

## Fallacy Detection

TruthGit includes pattern-based fallacy detection.

### Honest Assessment

**What it does:** Regex pattern matching for common fallacy structures.

**What it doesn't do:** Deep semantic understanding of arguments.

```python
# Example: This WILL be detected (obvious pattern)
detect_fallacies("He's an idiot, so his argument is wrong.")
# → AD_HOMINEM detected

# Example: This will NOT be detected (requires context)
detect_fallacies("His credentials are questionable, which affects credibility.")
# → No detection (subtle, may or may not be fallacious)
```

### Detected Patterns (11 types)

| Formal | Informal |
|--------|----------|
| Affirming the Consequent | Ad Hominem |
| Denying the Antecedent | Straw Man |
| False Dilemma | Appeal to Authority |
| Circular Reasoning | Slippery Slope |
| | Appeal to Emotion |
| | Hasty Generalization |
| | Red Herring |

**Limitation:** These are heuristics, not guarantees. False positives and false negatives are possible.

---

## Hypothesis Testing

TruthGit evaluates claims for falsifiability using keyword matching.

### Honest Assessment

**What it does:** Checks claims against keyword lists for known scientific concepts.

**What it doesn't do:** Query scientific databases or evaluate methodology.

```python
# This works (keyword match)
evaluate_hypothesis("Evolution explains biodiversity")
# → ESTABLISHED (contains "evolution")

# This is limited (no database lookup)
evaluate_hypothesis("CRISPR-Cas9 can edit genes")
# → May not classify correctly without specific keywords
```

### Epistemic Statuses

| Status | Meaning | How Determined |
|--------|---------|----------------|
| ESTABLISHED | Scientific consensus | Keyword match (evolution, gravity, etc.) |
| CONTESTED | Active debate | Keyword match (dark matter, consciousness) |
| SPECULATIVE | Untested | Default for testable claims |
| FRINGE | Contradicts consensus | Keyword match (flat earth, astrology) |
| UNFALSIFIABLE | Cannot be tested | Pattern match ("works in mysterious ways") |

**Limitation:** Keyword lists are not comprehensive. Novel or nuanced claims may be misclassified.

---

## Cryptographic Proofs

TruthGit generates SHA-256 hashes of verification records.

### What "Proof" Actually Means

```python
proof = hashlib.sha256(claim + verification_data).hexdigest()
```

| What It Proves | What It Doesn't Prove |
|----------------|----------------------|
| The data hasn't been tampered with | The claim is factually true |
| The verification record is consistent | The validators were correct |
| You can verify the hash matches | Anything about external reality |

**This is data integrity, not truth verification.**

---

## API & Deployment

### Cloud API

```
Base URL: https://truthgit-api-342668283383.us-central1.run.app
```

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Repository status |
| `/api/verify` | POST | Verify a claim |
| `/api/prove` | POST | Generate integrity hash |
| `/api/search` | GET | Search verified claims |

### Deploy Your Own

```bash
git clone https://github.com/lumensyntax/truthgit
cd truthgit
gcloud run deploy truthgit-api --source . --region us-central1
```

---

## Python API

```python
from truthgit import TruthRepository

repo = TruthRepository()
repo.init()

# Create and verify a claim
claim = repo.claim(content="E=mc²", domain="physics")

verification = repo.verify(
    verifier_results={
        "HERMES3": (0.95, "Mass-energy equivalence"),
        "NEMOTRON": (0.92, "Einstein's equation"),
    },
    claim_content="E=mc²",
    claim_domain="physics",
)

print(f"Consensus: {verification.consensus.value:.0%}")
# Consensus: 94%

# Check ontological classification
if verification.ontological_consensus:
    onto = verification.ontological_consensus
    print(f"Status: {onto.status}")
    print(f"Type: {onto.disagreement_type}")
```

---

## MCP Server

TruthGit includes an MCP server for Claude Desktop integration.

### Configuration

Add to `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "truthgit": {
      "command": "python",
      "args": ["-m", "truthgit.mcp_server"]
    }
  }
}
```

### Tools

| Tool | Description |
|------|-------------|
| `truthgit_verify_claim` | Multi-validator consensus check |
| `truthgit_prove` | Generate integrity hash |
| `truthgit_verify_proof` | Verify hash consistency |
| `truthgit_search` | Search verified claims |
| `truthgit_status` | Repository status |

---

## Architecture

### Storage Structure

```
.truth/
├── objects/
│   ├── cl/  # Claims
│   ├── ax/  # Axioms
│   ├── ct/  # Contexts
│   └── vf/  # Verifications
├── refs/
│   ├── consensus/
│   └── perspectives/
└── HEAD
```

### Verification Flow

```
        ┌─────────────┐
        │   Claim     │
        │  + Domain   │
        └──────┬──────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌───────┐  ┌───────┐  ┌───────┐
│ LLM A │  │ LLM B │  │ LLM C │
└───────┘  └───────┘  └───────┘
               │
               ▼
     ┌─────────────────┐
     │ Classification  │
     │ (PASSED/MYSTERY │
     │  /GAP/ERROR)    │
     └─────────────────┘
```

---

## Validators

### Local (No API Keys)

```python
from truthgit.validators import OllamaValidator

validators = [
    OllamaValidator("llama3"),
    OllamaValidator("mistral"),
]
```

### Cloud (Optional)

```python
from truthgit.validators import ClaudeValidator, GPTValidator

validators = [
    ClaudeValidator(),  # ANTHROPIC_API_KEY
    GPTValidator(),     # OPENAI_API_KEY
]
```

---

## Roadmap

**Completed:**
- [x] Ontological consensus classification
- [x] Pattern-based fallacy detection
- [x] Keyword-based hypothesis testing
- [x] MCP server integration
- [x] Cloud deployment

**Future (would address current limitations):**
- [ ] Integration with scientific databases (PubMed, Semantic Scholar)
- [ ] NLI-based fallacy detection (semantic, not regex)
- [ ] External fact-checking API integration
- [ ] Human-in-the-loop verification workflows

---

## Philosophy

TruthGit is built on these principles:

1. **Classification over binary** — "What type of disagreement?" matters more than "pass/fail"
2. **Transparency over magic** — Document limitations honestly
3. **Consensus over authority** — No single AI is trusted alone
4. **Immutability** — Verification history is append-only

### The Core Insight

Not all disagreement is equal:
- **LOGICAL_ERROR**: One validator made an obvious mistake
- **MYSTERY**: Genuinely unknowable (philosophical questions)
- **GAP**: Needs external information or human judgment

This classification is the actual value of TruthGit.

---

## Contributing

```bash
git clone https://github.com/lumensyntax/truthgit
cd truthgit
pip install -e ".[dev]"
pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT © [LumenSyntax](https://lumensyntax.dev)

---

<div align="center">

**TruthGit** — Consensus tracking for AI-assisted verification.

*Honest about what it does. Clear about what it doesn't.*

</div>
