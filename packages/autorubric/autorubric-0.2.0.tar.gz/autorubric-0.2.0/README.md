# AutoRubric

A Python library for evaluating text outputs against weighted criteria using LLM-as-a-judge.

---

<p align="center">
  <a href="https://pypi.org/project/autorubric/">
    <img src="https://img.shields.io/pypi/v/autorubric" alt="PyPI version" />
  </a>
  <a href="https://pypi.org/project/autorubric/">
    <img src="https://img.shields.io/pypi/pyversions/autorubric" alt="Python versions" />
  </a>
  <a href="https://github.com/delip/autorubric/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License" />
  </a>
</p>

## Installation

```bash
uv add autorubric
```

or

```bash
pip install autorubric
```

## Quick Start

```python
import asyncio
from autorubric import Rubric, LLMConfig
from autorubric.graders import CriterionGrader

async def main():
    # Configure LLM (model is required)
    grader = CriterionGrader(llm_config=LLMConfig(model="openai/gpt-4.1-mini"))

    # Build rubric for evaluating Li-ion battery cathode material comparison
    rubric = Rubric.from_dict([
        {"weight": 10.0, "requirement": "States NMC cell-level energy density in the 250-300 Wh/kg range"},
        {"weight": 8.0, "requirement": "Identifies LFP thermal runaway threshold (~270°C) as higher than NMC (~210°C)"},
        {"weight": 6.0, "requirement": "States LFP cycle life advantage (2000-5000 cycles vs 1000-2000 for NMC)"},
        {"weight": -15.0, "requirement": "Incorrectly claims LFP has higher gravimetric energy density than NMC"}
    ])

    # Grade a technical response
    result = await rubric.grade(
        to_grade="""NMC cathodes (LiNixMnyCozO2) achieve 250-280 Wh/kg at the cell level,
        while LFP (LiFePO4) typically reaches 150-205 Wh/kg. However, LFP offers superior
        thermal stability with decomposition onset at ~270°C compared to ~210°C for NMC,
        and delivers 2000-5000 charge cycles versus 1000-2000 for NMC.""",
        grader=grader,
        query="Compare NMC and LFP cathode materials for EV battery applications.",
    )

    print(f"Score: {result.score:.2f}")  # Score is 0.0-1.0
    for criterion in result.report:
        print(f"  [{criterion.final_verdict}] {criterion.criterion.requirement}")
        print(f"    -> {criterion.final_reason}")

asyncio.run(main())
```

## LLM Configuration

AutoRubric uses [LiteLLM](https://docs.litellm.ai/) under the hood, providing access to 100+ LLM providers with a unified interface.

### Supported Providers

| Provider | Model Format | Environment Variable |
|----------|-------------|---------------------|
| OpenAI | `openai/gpt-4.1`, `openai/gpt-4.1-mini` | `OPENAI_API_KEY` |
| Anthropic | `anthropic/claude-sonnet-4-5-20250929`, `anthropic/claude-opus-4-5-20251101` | `ANTHROPIC_API_KEY` |
| Google | `gemini/gemini-2.5-flash`, `gemini/gemini-2.5-pro` | `GEMINI_API_KEY` |
| Azure OpenAI | `azure/openai/gpt-4.1` | `AZURE_API_KEY`, `AZURE_API_BASE` |
| Groq | `groq/llama-3.1-70b-versatile` | `GROQ_API_KEY` |
| Ollama | `ollama/qwen3:14b`, `ollama/llama3` | (local, no key needed) |

See the [LiteLLM Provider Documentation](https://docs.litellm.ai/docs/providers) for the full list of supported providers.

### Environment Variables

Set API keys for your chosen provider:

```bash
# OpenAI
export OPENAI_API_KEY=your_key_here

# Anthropic
export ANTHROPIC_API_KEY=your_key_here

# Google
export GEMINI_API_KEY=your_key_here

# Azure OpenAI
export AZURE_API_KEY=your_key_here
export AZURE_API_BASE=https://your-resource.openai.azure.com

# Groq
export GROQ_API_KEY=your_key_here
```

AutoRubric automatically loads environment variables from `.env` files.

## LLMConfig Options

`LLMConfig` is the central configuration class for LLM calls:

```python
from autorubric import LLMConfig

config = LLMConfig(
    # REQUIRED - Model identifier in LiteLLM format
    model="openai/gpt-4.1-mini",

    # Sampling parameters
    temperature=0.0,           # 0.0 = deterministic (default)
    max_tokens=1024,           # Maximum tokens in response
    top_p=None,                # Nucleus sampling parameter

    # Request handling
    timeout=60.0,              # Request timeout in seconds
    max_retries=3,             # Retry attempts for transient failures

    # Rate limiting
    max_parallel_requests=None,  # Max concurrent requests per provider (None = unlimited)

    # Response caching (diskcache-based)
    cache_enabled=False,       # Enable response caching
    cache_dir=".autorubric_cache",  # Cache directory
    cache_ttl=None,            # Cache TTL in seconds (None = no expiration)

    # Thinking/Reasoning (unified across providers)
    thinking=None,             # "low", "medium", "high", or token budget (e.g., 32000)
    prompt_caching=True,       # Anthropic prompt caching (enabled by default)
    seed=None,                 # OpenAI reproducibility seed

    # Advanced options
    api_key=None,              # Override environment variable
    api_base=None,             # Custom API endpoint
    extra_headers={},          # Additional HTTP headers
    extra_params={},           # Additional provider-specific parameters
)
```

## YAML Configuration

Load LLM configuration from YAML files for easier management:

```yaml
# llm_config.yaml
model: openai/gpt-4.1
temperature: 0.0
max_tokens: 1024
cache_enabled: true
cache_ttl: 3600
```

```python
from autorubric import LLMConfig
from autorubric.graders import CriterionGrader

config = LLMConfig.from_yaml("llm_config.yaml")
grader = CriterionGrader(llm_config=config)
```

You can also save configurations:

```python
config = LLMConfig(model="openai/gpt-4.1", temperature=0.0)
config.to_yaml("llm_config.yaml")
```

## Grading Strategy

### CriterionGrader

A unified grader with compositional support for single LLM, ensemble, and few-shot modes. All combinations work orthogonally.

**Modes:**
- **Single LLM**: Use `llm_config` parameter
- **Ensemble**: Use `judges` parameter (list of JudgeSpec)
- **Few-shot**: Add `training_data` + `few_shot_config` (works with both modes)

**Position Bias Mitigation:**

For multi-choice criteria, LLMs can exhibit position bias (preferring earlier or later options). The `shuffle_options` parameter (enabled by default) randomly shuffles option order before presenting to the LLM, with responses mapped back to original indices for consistent metrics.

```python
# Default: shuffling enabled
grader = CriterionGrader(llm_config=LLMConfig(model="openai/gpt-4.1-mini"))

# Disable for deterministic behavior (e.g., in tests)
grader = CriterionGrader(
    llm_config=LLMConfig(model="openai/gpt-4.1-mini"),
    shuffle_options=False,
)
```

```python
from autorubric import LLMConfig, FewShotConfig
from autorubric.graders import CriterionGrader, JudgeSpec

# Single LLM mode
grader = CriterionGrader(
    llm_config=LLMConfig(model="gemini/gemini-3-flash-preview"),
)

# With custom system prompt
grader = CriterionGrader(
    llm_config=LLMConfig(model="openai/gpt-4.1-mini"),
    system_prompt="Optional custom system prompt",
)

# Ensemble mode with multiple judges
grader = CriterionGrader(
    judges=[
        JudgeSpec(LLMConfig(model="gemini/gemini-3-flash-preview"), "gemini", weight=1.0),
        JudgeSpec(LLMConfig(model="anthropic/claude-sonnet-4-5-20250929"), "claude", weight=1.2),
        JudgeSpec(LLMConfig(model="openai/gpt-4.1-mini"), "gpt-4.1", weight=1.0),
    ],
    aggregation="weighted",  # "majority", "weighted", "unanimous", "any"
)

# Single LLM + few-shot examples
train_data, test_data = dataset.split_train_test(n_train=100, stratify=True, seed=42)
grader = CriterionGrader(
    llm_config=LLMConfig(model="gemini/gemini-3-flash-preview"),
    training_data=train_data,
    few_shot_config=FewShotConfig(n_examples=3, balance_verdicts=True, seed=42),
)

# Ensemble + few-shot (all judges get the same examples)
grader = CriterionGrader(
    judges=[
        JudgeSpec(LLMConfig(model="gemini/gemini-3-flash-preview"), "gemini"),
        JudgeSpec(LLMConfig(model="anthropic/claude-sonnet-4-5-20250929"), "claude"),
    ],
    aggregation="majority",
    training_data=train_data,
    few_shot_config=FewShotConfig(n_examples=3),
)

result = await rubric.grade(to_grade=response, grader=grader)

# Result is always EnsembleEvaluationReport (consistent interface)
print(f"Score: {result.score:.3f}")
print(f"Mean Agreement: {result.mean_agreement:.1%}")  # 1.0 for single LLM
print(f"Judge Scores: {result.judge_scores}")  # Per-judge breakdown
```

**How it works:**
- Single LLM mode is internally treated as an "ensemble of 1"
- Makes one LLM call per criterion per judge concurrently via `asyncio.gather()`
- Returns `EnsembleEvaluationReport` with detailed per-criterion voting

**Why ensemble?** Research on LLM-as-a-judge evaluation consistently shows that **multi-LLM ensembles improve robustness** over single-model verdicts. Ensembles help mitigate self-preference bias, systematic blind spots, and position/order bias.

**Aggregation strategies:**

| Strategy | Description |
|----------|-------------|
| `majority` | > 50% of judges must vote MET |
| `weighted` | Weighted vote using judge weights |
| `unanimous` | All judges must vote MET |
| `any` | Any judge voting MET results in MET |

**EnsembleEvaluationReport fields:**

| Field | Description |
|-------|-------------|
| `score` | Final aggregated score |
| `raw_score` | Weighted sum before normalization |
| `mean_agreement` | Average agreement across all criteria (0-1) |
| `judge_scores` | Dict mapping judge_id to individual scores |
| `report` | List of `EnsembleCriterionReport` with per-criterion votes |
| `cannot_assess_count` | Number of criteria with CANNOT_ASSESS verdict |
| `token_usage` | Aggregated token usage |
| `completion_cost` | Total cost in USD |

### CANNOT_ASSESS Handling

When a judge cannot determine whether a criterion is met (e.g., insufficient evidence), it may return `CANNOT_ASSESS` instead of `MET` or `UNMET`. Configure how to handle these verdicts in score calculation:

```python
from autorubric import CannotAssessConfig, CannotAssessStrategy, LLMConfig
from autorubric.graders import CriterionGrader

# Default: skip unassessable criteria (adjust denominator)
grader = CriterionGrader(
    llm_config=LLMConfig(model="openai/gpt-4.1-mini"),
)

# Be conservative: treat cannot-assess as failure
grader = CriterionGrader(
    llm_config=LLMConfig(model="openai/gpt-4.1-mini"),
    cannot_assess_config=CannotAssessConfig(strategy=CannotAssessStrategy.FAIL),
)

# Give partial credit (30%)
grader = CriterionGrader(
    llm_config=LLMConfig(model="openai/gpt-4.1-mini"),
    cannot_assess_config=CannotAssessConfig(
        strategy=CannotAssessStrategy.PARTIAL,
        partial_credit=0.3
    ),
)
```

**Available strategies:**

| Strategy | Description |
|----------|-------------|
| `SKIP` | Exclude from scoring (adjust denominator) - default |
| `ZERO` | Treat as 0 contribution (same as UNMET) |
| `PARTIAL` | Treat as partial credit (configurable fraction) |
| `FAIL` | Treat as worst case (UNMET for positive, MET for negative weights) |

The `cannot_assess_count` field in the evaluation report shows how many criteria received this verdict.

**Scoring Formula:**

For each criterion $i$:

- If verdict = MET, contribution = $w_i$
- If verdict = UNMET, contribution = 0

Final score:

$$
\text{score} = \max\left(0, \min\left(1, \frac{\sum_{i=1}^{n} \mathbb{1}[\text{verdict}_i = \text{MET}] \cdot w_i}{\sum_{i=1}^{n} \max(0, w_i)}\right)\right)
$$

## Provider-Specific Features

### Extended Thinking/Reasoning

Research on LLM-as-a-judge evaluation (G-Eval, MT-Bench, and others) consistently shows that **reasoning before scoring improves evaluation quality**. When the judge model reasons through evidence systematically before committing to a verdict, it considers more evidence, catches its own mistakes, and produces more consistent evaluations. AutoRubric supports native model thinking across providers, which is more effective than prompt-based chain-of-thought because it uses each model's built-in reasoning capabilities.

Enable step-by-step reasoning for complex evaluations (works across providers):

```python
from autorubric import LLMConfig
from autorubric.graders import CriterionGrader

# Level-based (cross-provider)
grader = CriterionGrader(
    llm_config=LLMConfig(
        model="anthropic/claude-sonnet-4-5-20250929",
        thinking="high",  # "low", "medium", "high", or "none"
    )
)

# Token budget (for fine-grained control)
grader = CriterionGrader(
    llm_config=LLMConfig(
        model="anthropic/claude-opus-4-5-20251101",
        thinking=32000,  # Explicit token budget
    )
)
```

When `thinking` is enabled, the LLM reasons step-by-step before responding. The thinking trace is available in structured output types via the `reasoning` field. Supported providers: Anthropic (Claude), OpenAI (o-series), Gemini (2.5+), DeepSeek.

### Prompt Caching

Reduce latency and cost on repeated calls with the same system prompt. This is **enabled by default** for supported providers:

```python
grader = CriterionGrader(
    llm_config=LLMConfig(
        model="anthropic/claude-sonnet-4-5-20250929",
        prompt_caching=True,  # Default: enabled
    )
)
```

For Anthropic models, LLMClient automatically adds `cache_control` to the system message and includes the appropriate beta header.

### OpenAI Reproducibility

Use a seed for reproducible outputs:

```python
grader = CriterionGrader(
    llm_config=LLMConfig(
        model="openai/gpt-4.1",
        seed=42,  # Fixed seed for reproducibility
    )
)
```

## Response Caching

AutoRubric uses [diskcache](https://grantjenks.com/docs/diskcache/) for efficient, thread-safe response caching:

```python
from autorubric import LLMConfig
from autorubric.graders import CriterionGrader

grader = CriterionGrader(
    llm_config=LLMConfig(
        model="openai/gpt-4.1-mini",
        cache_enabled=True,          # Enable caching
        cache_dir=".autorubric_cache",  # Cache directory
        cache_ttl=3600,              # 1 hour TTL (None = no expiration)
    )
)

# The grader uses an LLMClient internally
# For direct client access:
from autorubric import LLMClient, LLMConfig

client = LLMClient(LLMConfig(model="openai/gpt-4.1-mini", cache_enabled=True))

# Cache management
client.clear_cache()       # Clear all cached responses
stats = client.cache_stats()  # Get cache statistics
# {'size': 1024, 'count': 10, 'directory': '.autorubric_cache'}
```

Cache keys are generated from model, system prompt, user prompt, and response format, ensuring identical requests return cached responses.

## Structured Outputs

AutoRubric uses Pydantic models for type-safe LLM responses. The grader automatically handles JSON parsing and validation:

```python
from autorubric import CriterionJudgment  # Single criterion judgment

# CriterionJudgment contains:
# - criterion_status: CriterionVerdict (MET or UNMET)
# - explanation: str (why the criterion was met or not)
# - reasoning: str | None (thinking trace when thinking is enabled)
```

This type is used internally by the grader but is exported for custom implementations.

## Score Fields

The `EvaluationReport` returned by `rubric.grade()` contains several score fields:

| Field | Description |
|-------|-------------|
| `score` | Final score (0-1 if normalized, raw weighted sum if `normalize=False`) |
| `raw_score` | Weighted sum before normalization |
| `llm_raw_score` | Same as raw_score (for consistency) |
| `report` | Per-criterion breakdown with verdicts and explanations |
| `error` | Error message if grading failed (e.g., JSON parse error). Filter these in training. |
| `token_usage` | Aggregated token usage across all LLM calls (see Usage Tracking section) |
| `completion_cost` | Total cost in USD for all LLM calls (see Usage Tracking section) |

## Usage Tracking

AutoRubric automatically tracks token usage and completion cost for all grading operations using LiteLLM's built-in usage tracking.

### Accessing Usage Data

The `EvaluationReport` includes `token_usage` and `completion_cost` fields:

```python
import asyncio
from autorubric import Rubric, LLMConfig
from autorubric.graders import CriterionGrader

async def main():
    grader = CriterionGrader(llm_config=LLMConfig(model="openai/gpt-4.1-mini"))
    rubric = Rubric.from_dict([
        {"weight": 10.0, "requirement": "States the correct answer"},
        {"weight": 5.0, "requirement": "Provides clear explanation"},
    ])

    result = await rubric.grade(
        to_grade="The answer is 42 because...",
        grader=grader,
    )

    print(f"Score: {result.score:.2f}")

    # Access token usage
    if result.token_usage:
        print(f"Prompt tokens: {result.token_usage.prompt_tokens}")
        print(f"Completion tokens: {result.token_usage.completion_tokens}")
        print(f"Total tokens: {result.token_usage.total_tokens}")

    # Access completion cost
    if result.completion_cost:
        print(f"Cost: ${result.completion_cost:.6f}")

asyncio.run(main())
```

### TokenUsage Fields

The `TokenUsage` dataclass contains:

| Field | Description |
|-------|-------------|
| `prompt_tokens` | Number of tokens in the prompt/input |
| `completion_tokens` | Number of tokens in the completion/output |
| `total_tokens` | Total tokens (prompt + completion) |
| `cache_creation_input_tokens` | Tokens used to create cache entries (Anthropic) |
| `cache_read_input_tokens` | Tokens read from cache (Anthropic) |

### Aggregating Usage Across Multiple Grading Operations

For batch grading, use the helper functions to aggregate usage:

```python
import asyncio
from autorubric import (
    Rubric, LLMConfig, TokenUsage,
    aggregate_token_usage, aggregate_completion_cost, aggregate_evaluation_usage
)
from autorubric.graders import CriterionGrader

async def batch_grade_with_usage():
    grader = CriterionGrader(llm_config=LLMConfig(model="openai/gpt-4.1-mini"))
    rubric = Rubric.from_file("rubric.yaml")

    responses = ["Response 1...", "Response 2...", "Response 3..."]

    # Grade all responses
    tasks = [rubric.grade(to_grade=r, grader=grader) for r in responses]
    results = await asyncio.gather(*tasks)

    # Aggregate usage and cost
    total_usage, total_cost = aggregate_evaluation_usage(results)

    if total_usage:
        print(f"Total tokens used: {total_usage.total_tokens}")
    if total_cost:
        print(f"Total cost: ${total_cost:.4f}")

    # Or aggregate manually
    usages = [r.token_usage for r in results]
    costs = [r.completion_cost for r in results]

    total_usage = aggregate_token_usage(usages)
    total_cost = aggregate_completion_cost(costs)
```

### Cost Calculation

Completion cost is calculated using LiteLLM's `completion_cost()` function, which has built-in pricing data for all supported providers. The cost is in USD.

**Note:** Cost calculation may return `None` if:
- The provider doesn't report usage data
- The model's pricing is not in LiteLLM's database
- An error occurs during calculation

## Length Penalty

Length penalty discourages excessively verbose outputs during evaluation. It is configured on the **grader constructor** and is subtracted from the score after grading.

### Configuration

```python
from autorubric import LengthPenalty

penalty = LengthPenalty(
    free_budget=6000,        # No penalty below this count
    max_cap=8000,            # Maximum penalty at/above this count
    penalty_at_cap=0.5,      # Max penalty to subtract from score
    exponent=1.6,            # Curve steepness (higher = more lenient near budget)
    count_fn=None,           # Custom counting function (default: word count)
    penalty_type="ALL",      # Which sections to count: "ALL", "OUTPUT_ONLY", "THINKING_ONLY"
)
```

### Usage

```python
from autorubric import Rubric, LLMConfig, LengthPenalty
from autorubric.graders import CriterionGrader

rubric = Rubric.from_file("rubric.yaml")

# With length penalty
grader = CriterionGrader(
    llm_config=LLMConfig(model="openai/gpt-4.1-mini"),
    length_penalty=LengthPenalty()
)
result = await rubric.grade(to_grade=response, grader=grader)

# With custom tokenizer
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

grader = CriterionGrader(
    llm_config=LLMConfig(model="openai/gpt-4.1-mini"),
    length_penalty=LengthPenalty(
        free_budget=8000,
        max_cap=10000,
        count_fn=lambda t: len(tokenizer.encode(t))
    )
)
result = await rubric.grade(to_grade=response, grader=grader)
```

### Penalty Formula

```
if count <= free_budget:
    penalty = 0
elif count >= max_cap:
    penalty = penalty_at_cap
else:
    frac = (count - free_budget) / (max_cap - free_budget)
    penalty = penalty_at_cap * (frac ** exponent)

final_score = max(0.0, base_score - penalty)
```

## Thinking/Output Token Support

For models that generate thinking/reasoning steps separately from final output (e.g., Claude with extended thinking), you can apply length penalties to specific sections.

### Input Formats

```python
# Dict format (explicit)
await rubric.grade(
    to_grade={
        "thinking": "Let me reason through this step by step...",
        "output": "The final answer is 42"
    },
    grader=grader
)

# String with markers (auto-parsed)
await rubric.grade(
    to_grade="<thinking>My reasoning process...</thinking><output>Final answer</output>",
    grader=grader
)

# Plain string (backwards compatible)
await rubric.grade(to_grade="Just a regular response", grader=grader)  # Treated as all output
```

### Penalty Type Selection

```python
penalty = LengthPenalty(
    free_budget=8000,
    max_cap=10000,
    penalty_at_cap=0.5,
    penalty_type="OUTPUT_ONLY"  # Options: "ALL", "OUTPUT_ONLY", "THINKING_ONLY"
)
```

- `"ALL"` - Count both thinking and output tokens (default)
- `"OUTPUT_ONLY"` - Only count output tokens (useful for RL training to allow long reasoning)
- `"THINKING_ONLY"` - Only count thinking tokens

## Training / RL Use Cases

For reinforcement learning training, normalized 0-1 scores can make optimization difficult. Use `normalize=False` to get raw weighted sums:

```python
from autorubric import Rubric, LLMConfig, LengthPenalty
from autorubric.graders import CriterionGrader
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("your-model")

grader = CriterionGrader(
    llm_config=LLMConfig(model="openai/gpt-4.1-mini"),
    normalize=False,  # Return raw weighted sums
    length_penalty=LengthPenalty(
        free_budget=8000,
        max_cap=10000,
        penalty_at_cap=50.0,  # Absolute penalty for raw scores
        exponent=1.6,
        count_fn=lambda text: len(tokenizer.encode(text, add_special_tokens=False))
    )
)

rubric = Rubric.from_file("rubric.yaml")
result = await rubric.grade(to_grade=response, grader=grader)

# result.score = raw weighted sum - length penalty
# result.raw_score = raw weighted sum (before length penalty)
```

### Batch Processing

```python
import asyncio

async def compute_rewards_batch(
    responses: list[str],
    rubrics: list[Rubric],
    grader: CriterionGrader,
    queries: list[str] | None = None,
) -> list[float]:
    tasks = []
    for i, (response, rubric) in enumerate(zip(responses, rubrics)):
        query = queries[i] if queries else None
        tasks.append(rubric.grade(to_grade=response, grader=grader, query=query))

    results = await asyncio.gather(*tasks)
    return [r.score for r in results]
```

### Key Differences from Normalized Mode

| Aspect | Normalized (default) | Training (normalize=False) |
|--------|---------------------|---------------------------|
| Score range | 0.0 to 1.0 | Can be negative or > 1 |
| Length penalty | Fractional (e.g., 0.5) | Absolute (e.g., 50.0) |
| Clamping | Score clamped to [0, 1] | No clamping |
| Use case | Evaluation, reporting | RL reward signals |

## Batch Evaluation with EvalRunner

For high-throughput evaluation of datasets, use `EvalRunner` or the `evaluate()` convenience function. Features include:
- Parallel execution with rate limiting
- Rich progress bars
- Checkpointing and resumption
- Timing statistics and cost aggregation

### Basic Usage

```python
import asyncio
from autorubric import RubricDataset, LLMConfig
from autorubric.graders import CriterionGrader
from autorubric import evaluate

async def main():
    dataset = RubricDataset.from_file("essays.json")
    grader = CriterionGrader(
        llm_config=LLMConfig(
            model="openai/gpt-4.1-mini",
            max_parallel_requests=10,  # Rate limit per provider
        )
    )

    result = await evaluate(dataset, grader, show_progress=True)

    print(f"Evaluated {result.successful_items}/{result.total_items}")
    print(f"Throughput: {result.timing_stats.items_per_second:.2f} items/s")
    print(f"Total cost: ${result.total_completion_cost:.4f}")

asyncio.run(main())
```

### Rate Limiting

Use `max_parallel_requests` in `LLMConfig` to limit concurrent API calls per provider:

```python
from autorubric import LLMConfig
from autorubric.graders import CriterionGrader, JudgeSpec

grader = CriterionGrader(
    judges=[
        JudgeSpec(LLMConfig(model="openai/gpt-4.1", max_parallel_requests=10), "gpt-4"),
        JudgeSpec(LLMConfig(model="anthropic/claude-sonnet-4-5-20250929", max_parallel_requests=5), "claude"),
    ],
    aggregation="majority",
)
```

The rate limiter uses a global per-provider semaphore, so all `openai/*` models share the same limit.

### Checkpointing and Resumption

EvalRunner automatically saves progress to disk, allowing resumption after interruptions:

```python
from autorubric import EvalRunner, EvalConfig, EvalResult

# First run (may be interrupted)
config = EvalConfig(
    experiment_name="my-essay-eval",  # Or None for auto-generated name
    experiments_dir="./experiments",
    show_progress=True,
)
runner = EvalRunner(dataset=dataset, grader=grader, config=config)
result = await runner.run()
# Saves to: experiments/my-essay-eval/manifest.json + items.jsonl

# Resume after crash (same config)
runner = EvalRunner(dataset=dataset, grader=grader, config=config)
result = await runner.run()  # Skips already-completed items

# Load results later
result = EvalResult.from_experiment("experiments/my-essay-eval")
```

### EvalConfig Options

| Option | Default | Description |
|--------|---------|-------------|
| `fail_fast` | `False` | Stop on first error |
| `show_progress` | `True` | Display progress bars |
| `progress_style` | `"simple"` | `"simple"` or `"detailed"` progress display |
| `max_concurrent_items` | `None` | Limit in-flight items (None = unlimited) |
| `experiment_name` | `None` | Name for experiment (auto-generated if None) |
| `experiments_dir` | `"experiments"` | Root directory for checkpoints |
| `resume` | `True` | Resume from checkpoint if exists |

### EvalResult Fields

| Field | Description |
|-------|-------------|
| `item_results` | List of `ItemResult` with per-item reports |
| `total_items` | Number of items in dataset |
| `successful_items` | Items graded successfully |
| `failed_items` | Items that failed to grade |
| `total_token_usage` | Aggregated token usage |
| `total_completion_cost` | Total cost in USD |
| `timing_stats` | `EvalTimingStats` with duration metrics |
| `started_at` / `completed_at` | Timestamps |
| `errors` | List of `(item_idx, error_message)` tuples |

### Timing Statistics

`EvalTimingStats` provides performance metrics:

```python
result = await evaluate(dataset, grader)
stats = result.timing_stats

print(f"Total time: {stats.total_duration_seconds:.1f}s")
print(f"Mean per item: {stats.mean_item_duration_seconds:.2f}s")
print(f"P95 latency: {stats.p95_item_duration_seconds:.2f}s")
print(f"Throughput: {stats.items_per_second:.2f} items/s")
```

## Evaluation Metrics

When your dataset includes ground truth labels, use `compute_metrics()` to measure how well your LLM judge agrees with human annotations.

### Basic Usage

```python
from autorubric import RubricDataset, LLMConfig, evaluate
from autorubric.graders import CriterionGrader

dataset = RubricDataset.from_file("data_with_ground_truth.json")
grader = CriterionGrader(llm_config=LLMConfig(model="openai/gpt-4.1-mini"))

result = await evaluate(dataset, grader, show_progress=True)

# Compute metrics against ground truth
metrics = result.compute_metrics(dataset)

# Formatted summary
print(metrics.summary())

# Export to pandas DataFrame
df = metrics.to_dataframe()

# Save to JSON file
metrics.to_file("metrics.json")
```

### MetricsResult Fields

| Field | Description |
|-------|-------------|
| `criterion_accuracy` | Overall accuracy across all criteria |
| `criterion_precision` | Precision for MET class |
| `criterion_recall` | Recall for MET class |
| `criterion_f1` | F1 score for MET class |
| `mean_kappa` | Mean Cohen's kappa across criteria |
| `per_criterion` | List of `CriterionMetrics` with per-criterion breakdown |
| `score_rmse` | RMSE of cumulative scores |
| `score_mae` | MAE of cumulative scores |
| `score_spearman` | Spearman rank correlation |
| `score_kendall` | Kendall tau correlation |
| `score_pearson` | Pearson correlation |
| `bias` | Systematic bias analysis (`BiasResult`) |
| `bootstrap` | Bootstrap confidence intervals (if enabled) |
| `per_judge` | Per-judge metrics for ensemble (if enabled) |
| `n_items` | Number of items evaluated |
| `n_criteria` | Number of criteria |
| `warnings` | Any warnings (e.g., missing items) |

### Bootstrap Confidence Intervals

Enable bootstrap for confidence intervals on key metrics:

```python
metrics = result.compute_metrics(
    dataset,
    bootstrap=True,       # Enable bootstrap CIs
    n_bootstrap=1000,     # Number of bootstrap samples (default: 1000)
    confidence_level=0.95,  # 95% CI (default)
    seed=42,              # For reproducibility
)

print(metrics.summary())
# Output includes:
# Bootstrap CIs (95%):
#   Accuracy: [85.2%, 92.1%]
#   Kappa:    [0.712, 0.845]
#   RMSE:     [0.0523, 0.0891]
```

### Per-Judge Metrics (Ensemble)

For ensemble evaluations, get metrics for each judge:

```python
from autorubric.graders import CriterionGrader, JudgeSpec

grader = CriterionGrader(
    judges=[
        JudgeSpec(LLMConfig(model="openai/gpt-4.1"), "gpt-4"),
        JudgeSpec(LLMConfig(model="anthropic/claude-sonnet-4-5-20250929"), "claude"),
    ],
    aggregation="majority",
)

result = await evaluate(dataset, grader)

metrics = result.compute_metrics(
    dataset,
    per_judge=True,  # Include per-judge metrics
)

# Access per-judge metrics
for judge_id, jm in metrics.per_judge.items():
    print(f"{judge_id}: Accuracy={jm.criterion_accuracy:.1%}, RMSE={jm.score_rmse:.4f}")
```

### Output Methods

```python
# Formatted text summary
print(metrics.summary())

# Export to pandas DataFrame (rows for aggregate, per-criterion, per-judge)
df = metrics.to_dataframe()

# Save to JSON file
metrics.to_file("results/metrics.json")
```

## Loading Rubrics

```python
from autorubric import Rubric, Criterion

# Direct construction (with optional name field)
rubric = Rubric([
    Criterion(name="margin", weight=10.0, requirement="States Q4 2023 base margin as 17.2%"),
    Criterion(name="attribution", weight=8.0, requirement="Explicitly uses Shapley attribution for decomposition"),
    Criterion(name="error_deliveries", weight=-15.0, requirement="Uses total deliveries instead of cash-only deliveries")
])

# From list of dictionaries (name field is optional)
rubric = Rubric.from_dict([
    {"name": "margin", "weight": 10.0, "requirement": "States Q4 2023 base margin as 17.2%"},
    {"name": "attribution", "weight": 8.0, "requirement": "Explicitly uses Shapley attribution for decomposition"},
    {"weight": -15.0, "requirement": "Uses total deliveries instead of cash-only deliveries"}  # name is optional
])

# From JSON string
rubric = Rubric.from_json('[{"weight": 10.0, "requirement": "Example requirement"}]')

# From YAML string
yaml_data = '''
- weight: 10.0
  requirement: "Example requirement"
'''
rubric = Rubric.from_yaml(yaml_data)

# From files
rubric = Rubric.from_file('rubric.json')
rubric = Rubric.from_file('rubric.yaml')
```

### JSON Format

```json
[
  {
    "name": "margin",
    "weight": 10.0,
    "requirement": "States Q4 2023 base margin as 17.2%"
  },
  {
    "name": "attribution",
    "weight": 8.0,
    "requirement": "Explicitly uses Shapley attribution for decomposition"
  },
  {
    "weight": -15.0,
    "requirement": "Uses total deliveries instead of cash-only deliveries"
  }
]
```

Note: The `name` field is optional. When provided, it can be used to reference criteria in reports.

Note: The `weight` field is optional and defaults to `10.0`. This enables uniform weighting when all criteria should be equally important:

```python
# Uniform weighting - all criteria equally important (weight defaults to 10.0)
rubric = Rubric.from_dict([
    {"requirement": "Is factually accurate"},
    {"requirement": "Is clearly written"},
    {"requirement": "Addresses the question"},
])
```

### YAML Format

```yaml
- name: margin        # Optional identifier
  weight: 10.0
  requirement: "States Q4 2023 base margin as 17.2%"
- name: attribution
  weight: 8.0
  requirement: "Explicitly uses Shapley attribution for decomposition"
- weight: -15.0       # name is optional
  requirement: "Uses total deliveries instead of cash-only deliveries"
```

### Sectioned Format

You can organize criteria into sections for better readability:

```yaml
# rubric.yaml with sections
rubric:
  sections:
    - name: "Accuracy"
      criteria:
        - weight: 10.0
          requirement: "States the correct answer"
        - weight: 5.0
          requirement: "Provides supporting evidence"
    - name: "Errors"
      criteria:
        - weight: -15.0
          requirement: "Contains factual errors"
```

Or as a JSON object:

```json
{
  "rubric": {
    "sections": [
      {
        "name": "Accuracy",
        "criteria": [
          {"weight": 10.0, "requirement": "States the correct answer"}
        ]
      }
    ]
  }
}
```

Criteria from all sections are flattened during evaluation.

## Error Handling

### Parse Failure Behavior

When the LLM returns invalid JSON or the response cannot be parsed, the grader uses **conservative defaults** to avoid biasing scores:

| Criterion Type | Default Verdict | Rationale |
|---------------|-----------------|-----------|-
| Positive (weight > 0) | UNMET | Assume requirement not met |
| Negative (weight < 0) | MET | Assume error is present |

This ensures parse failures result in worst-case scores rather than artificially inflating results.

## Dataset Support

AutoRubric provides classes for organizing evaluation datasets with ground truth labels:

```python
from autorubric import Rubric, Criterion, CriterionVerdict, DataItem, RubricDataset

# Create a rubric
rubric = Rubric([
    Criterion(name="Accuracy", weight=10.0, requirement="Factually correct"),
    Criterion(name="Clarity", weight=5.0, requirement="Clear and concise"),
])

# Create a dataset
dataset = RubricDataset(
    name="photosynthesis-eval",  # Optional name for identification
    prompt="Explain photosynthesis",
    rubric=rubric,
)

# Add items with ground truth
dataset.add_item(
    text="Photosynthesis is the process by which plants convert sunlight...",
    description="Good response",
    ground_truth=[CriterionVerdict.MET, CriterionVerdict.MET]
)

# Serialize to JSON
json_str = dataset.to_json()
dataset.to_file("dataset.json")

# Load from JSON
loaded = RubricDataset.from_json(json_str)
loaded = RubricDataset.from_file("dataset.json")

# Compute scores from verdicts
score = dataset.compute_weighted_score(
    [CriterionVerdict.MET, CriterionVerdict.UNMET],
    normalize=True
)
```

### Per-Item Rubrics

For datasets where each item requires a unique rubric (e.g., question-specific evaluation criteria), use per-item rubrics:

```python
from autorubric import Rubric, Criterion, DataItem, RubricDataset

# Create items with individual rubrics
item1 = DataItem(
    text="Answer to question 1...",
    description="Q1",
    rubric=Rubric([
        Criterion(name="Accuracy", weight=1.0, requirement="Correct answer for Q1"),
    ])
)

item2 = DataItem(
    text="Answer to question 2...",
    description="Q2",
    rubric=Rubric([
        Criterion(name="Relevance", weight=2.0, requirement="Relevant to Q2"),
        Criterion(name="Depth", weight=1.0, requirement="Provides depth for Q2"),
    ])
)

# Create dataset with no global rubric (all items have their own)
dataset = RubricDataset(
    prompt="Answer the question",
    rubric=None,  # No global rubric needed
    items=[item1, item2],
)

# Get effective rubric for an item
rubric = dataset.get_item_rubric(0)  # Returns item1's rubric
```

When loading from JSON, if both the global rubric and an item's rubric are `None`, a `ValueError` is raised:

```json
{
  "prompt": "Answer the question",
  "rubric": null,
  "items": [
    {
      "text": "Response text",
      "description": "Q1",
      "rubric": [{"name": "Accuracy", "weight": 1.0, "requirement": "..."}]
    }
  ]
}
```

### Generating Synthetic Ground Truth

When you have a dataset without ground truth labels, use `fill_ground_truth()` to automatically generate them using an LLM grader:

```python
import asyncio
from autorubric import RubricDataset, LLMConfig
from autorubric.graders import CriterionGrader
from autorubric.utils import fill_ground_truth

async def main():
    # Load unlabeled dataset
    dataset = RubricDataset.from_file("unlabeled.json")

    # Use a strong model for ground truth generation
    grader = CriterionGrader(
        llm_config=LLMConfig(
            model="anthropic/claude-sonnet-4-5-20250929",
            max_parallel_requests=10,
        )
    )

    # Generate ground truth (items without ground_truth will be graded)
    labeled = await fill_ground_truth(
        dataset,
        grader,
        force=False,        # Only label items without ground_truth
        show_progress=True,
    )

    # Items that failed to grade are excluded from the result
    print(f"Labeled {len(labeled)} of {len(dataset)} items")

    # Save the labeled dataset
    labeled.to_file("labeled.json")

asyncio.run(main())
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `force` | `False` | If True, re-grade all items. If False, skip items with existing ground_truth |
| `show_progress` | `True` | Display a progress bar |
| `max_concurrent_items` | `None` | Limit concurrent grading (None = unlimited) |

**Behavior:**
- Returns a new `RubricDataset` (original is not modified)
- Items that fail to grade are excluded from the returned dataset
- Items with existing ground_truth are preserved (unless `force=True`)
- For binary criteria, ground_truth contains `CriterionVerdict` values
- For multi-choice criteria, ground_truth contains option label strings

## Multi-Choice Criteria

Beyond binary MET/UNMET verdicts, autorubric supports multi-choice criteria for:
- **Ordinal scales**: Satisfaction ratings (1-4), quality levels with values 0.0-1.0
- **Nominal scales**: Categorical judgments where multiple options can have the same value
- **NA options**: Options excluded from scoring (like CANNOT_ASSESS for binary criteria)

### Ordinal Scale Example (YAML)

```yaml
criteria:
  - name: satisfaction
    requirement: "How satisfied would you be with this response?"
    weight: 10.0
    scale_type: ordinal
    options:
      - label: "1"
        value: 0.0
      - label: "2"
        value: 0.33
      - label: "3"
        value: 0.67
      - label: "4"
        value: 1.0
```

### Nominal Scale Example (YAML)

```yaml
criteria:
  - name: efficiency
    requirement: "Is the number of exchange turns appropriate?"
    weight: 5.0
    scale_type: nominal
    options:
      - label: "Too few interactions"
        value: 0.0
      - label: "Too many interactions"
        value: 0.0
      - label: "Just right"
        value: 1.0
```

### NA Options

Add `na: true` to exclude an option from scoring:

```yaml
options:
  - label: "None"
    value: 0.0
  - label: "All claims"
    value: 1.0
  - label: "NA - No references provided"
    na: true  # Excluded from scoring
```

### Ensemble Aggregation

For multi-choice criteria in ensemble mode, configure aggregation strategies:

```python
grader = CriterionGrader(
    judges=[...],
    aggregation="majority",           # For binary criteria
    ordinal_aggregation="mean",       # For ordinal: "mean", "median", "weighted_mean", "mode"
    nominal_aggregation="mode",       # For nominal: "mode", "weighted_mode", "unanimous"
)
```

### Ground Truth Format

Ground truth for multi-choice criteria uses option labels (strings):

```python
dataset.add_item(
    text="Response text...",
    description="Good response",
    ground_truth=[
        CriterionVerdict.MET,  # Binary criterion
        "4",                    # Multi-choice: satisfaction (ordinal)
        "Just right",           # Multi-choice: efficiency (nominal)
    ]
)
```

See CLAUDE.md for detailed documentation on multi-choice types, aggregation strategies, and position bias mitigation.

## Public Exports

```python
from autorubric import (
    # Dataset classes
    DataItem,
    RubricDataset,

    # LLM Infrastructure
    GenerateResult,
    LLMClient,
    LLMConfig,
    ThinkingConfig,
    ThinkingLevel,
    ThinkingLevelLiteral,
    ThinkingParam,
    generate,

    # Core types
    Rubric,
    Criterion,
    CriterionJudgment,
    CriterionReport,
    CriterionVerdict,
    EvaluationReport,
    LengthPenalty,
    CountFn,
    TokenUsage,

    # CANNOT_ASSESS handling
    CannotAssessConfig,
    CannotAssessStrategy,

    # Few-shot types
    FewShotConfig,
    FewShotExample,

    # Ensemble types
    AggregationStrategy,
    EnsembleCriterionReport,
    EnsembleEvaluationReport,
    JudgeVote,

    # Thinking/output support
    PenaltyType,
    ThinkingOutputDict,
    ToGradeInput,

    # Evaluation runner
    EvalConfig,
    EvalResult,
    EvalRunner,
    EvalTimingStats,
    ExperimentManifest,
    ItemResult,
    evaluate,

    # Evaluation metrics
    compute_metrics,
    MetricsResult,
    CriterionMetrics,
    JudgeMetrics,
    BiasResult,
    BootstrapResults,
    CorrelationResult,

    # Utility functions
    aggregate_completion_cost,
    aggregate_evaluation_usage,
    aggregate_token_usage,
    compute_length_penalty,
    fill_ground_truth,
    normalize_to_grade_input,
    parse_thinking_output,
    word_count,
)

from autorubric.graders import (
    CriterionGrader,
    Grader,
    JudgeSpec,
)
```

## Requirements

- Python 3.11+
- [LiteLLM](https://docs.litellm.ai/) for multi-provider LLM support
- [diskcache](https://grantjenks.com/docs/diskcache/) for response caching
- [Pydantic](https://docs.pydantic.dev/) for structured outputs
- [tenacity](https://tenacity.readthedocs.io/) for retry logic
- [rich](https://rich.readthedocs.io/) for progress bars
- [coolname](https://github.com/alexanderlukanin13/coolname) for experiment naming

## License

MIT License - see LICENSE file for details.
