# Evaluation Module

This module provides comprehensive evaluation tools for the psychological counseling system.

---

## Quick Start

### Run Quick Test

```bash
python evaluation/scripts/run_quick_test.py
```

### Run Full Evaluation

```bash
python examples/comparison_experiment.py
```

---

## Module Structure

```
evaluation/
├── configs/                  # Evaluation configurations
│   ├── default_config.yaml
│   ├── quick_test_config.yaml
│   └── comparison_config.yaml
│
├── datasets/                 # Dataset loaders and test data
│   ├── dataset_loader.py
│   ├── download_datasets.py
│   └── comparison_test_questions.json
│
├── metrics/                  # Evaluation metrics
│   ├── technical_metrics.py  # Response time, length, etc.
│   ├── clinical_metrics.py   # Professionalism, empathy, etc.
│   ├── memory_metrics.py     # Memory recall, personalization
│   └── rag_metrics.py        # Retrieval quality
│
├── evaluators/              # Evaluation orchestration
│   ├── system_evaluator.py
│   └── comparison_evaluator.py
│
├── scripts/                 # Evaluation scripts
│   └── run_quick_test.py
│
└── results/                 # Evaluation results (auto-created)
    ├── quick_test/
    └── comparison/
```

---

## Evaluation Metrics

### Technical Metrics

- Response time
- Response length
- Context utilization
- Token efficiency

### Clinical Metrics

- Professionalism (1-5)
- Empathy (1-5)
- Actionability (1-5)
- Safety

### Memory Metrics

- Recall accuracy
- Personalization level
- Continuity score

### RAG Metrics

- Retrieval precision
- Knowledge utilization
- Context relevance

---

## Usage

### Basic Evaluation

```python
from evaluation import SystemEvaluator

evaluator = SystemEvaluator(config)

result = evaluator.evaluate(
    test_case={
        "user_message": "I feel anxious",
        "expected_keywords": ["anxiety", "breathing", "techniques"]
    }
)

print(result.metrics)
```

### Comparison Evaluation

```python
from evaluation import ComparisonEvaluator

evaluator = ComparisonEvaluator()

result = evaluator.compare_configurations(
    configs=[config_bare, config_rag, config_full],
    test_cases=test_cases
)

print(result.summary)
```

---

## Configuration

Edit `evaluation/configs/` files to customize:

- Test datasets
- Evaluation metrics
- LLM judge settings
- Output formats

---

## Datasets

### Built-in Test Sets

- `comparison_test_questions.json`: 10 curated test cases
- Generated memory tests: Multi-session scenarios

### External Datasets

Download additional datasets:

```bash
python evaluation/datasets/download_datasets.py --dataset mentalchat
```

Available:
- MentalChat16K
- Counsel Chat
- Empathetic Dialogues

---

## Results Format

Results are saved in JSON and Markdown formats:

```
evaluation/results/
└── comparison_2024-01-15/
    ├── metrics.json          # Quantitative metrics
    ├── responses.json        # Full responses
    ├── summary.md           # Human-readable summary
    └── figures/             # Visualizations
```

---

## Further Reading

- [Evaluation Guide](../docs/evaluation.md) - Detailed evaluation guide
- [Metrics Documentation](metrics/) - Metric implementations
- [Paper Results](../experiments/) - Reproduced paper results

---

For more information, see the [main documentation](../docs/).
