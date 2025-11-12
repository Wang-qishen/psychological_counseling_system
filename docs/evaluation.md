# Evaluation Guide

Guide to reproducing experiments from our paper and evaluating the system.

---

## Table of Contents

- [Quick Test](#quick-test)
- [Comparison Experiment](#comparison-experiment)
- [Case Studies](#case-studies)
- [Evaluation Metrics](#evaluation-metrics)
- [Custom Evaluation](#custom-evaluation)

---

## Quick Test

Run a quick 5-minute test to verify the system works:

```bash
python evaluation/scripts/run_quick_test.py
```

This tests all core components with a small dataset.

**Output:**
```
evaluation/results/quick_test/
├── quick_test_2024-01-15_10-30-00.json
└── metrics_summary.txt
```

---

## Comparison Experiment

**Paper Section**: Section 4.1 - Comparison Experiment

This experiment compares three configurations:
1. **Bare LLM**: No RAG, no memory
2. **LLM + RAG**: With knowledge retrieval
3. **Full System**: RAG + memory

### Running the Experiment

```bash
python examples/comparison_experiment.py
```

### Configuration

Edit `evaluation/configs/comparison_config.yaml`:

```yaml
scenarios:
  - name: "work_stress_insomnia"
    initial_profile:
      age: 28
      gender: "female"
      occupation: "software engineer"
      main_issues: ["work_stress", "insomnia"]
    
  questions:
    - "I've been having trouble sleeping lately..."
    - "Work has been really stressful..."
```

### Results

Results saved to `experiments/`:

```
experiments/
├── comparison_report_2024-01-15.json
├── detailed_comparison.md
├── response_examples.md
└── figures/
    ├── response_time_comparison.png
    ├── response_length_comparison.png
    └── scenario_comparison.png
```

### Evaluation Metrics

- **Professionalism**: Use of evidence-based techniques
- **Personalization**: Reference to user history
- **Actionability**: Concrete suggestions
- **Empathy**: Emotional understanding

Rated by GPT-4 on 1-5 scale.

---

## Case Studies

**Paper Section**: Section 4.2 - Case Analysis

### Run Specific Scenarios

```bash
# Social anxiety case
python examples/case_study.py --scenario social_anxiety

# Postpartum depression case
python examples/case_study.py --scenario postpartum_depression

# Exam anxiety case
python examples/case_study.py --scenario exam_anxiety
```

### Custom Case Study

```python
from evaluation.evaluators import SystemEvaluator

evaluator = SystemEvaluator(config)

result = evaluator.evaluate_case(
    user_profile={
        "age": 28,
        "occupation": "teacher",
        "main_issues": ["work_stress", "relationship"]
    },
    conversation=[
        {"role": "user", "content": "I'm having problems at work..."},
        # ... more turns
    ]
)

print(result.metrics)
```

---

## Evaluation Metrics

### Technical Metrics

Implemented in `evaluation/metrics/technical_metrics.py`:

```python
from evaluation.metrics import TechnicalMetrics

metrics = TechnicalMetrics()

# Response time
time = metrics.measure_response_time(dialogue_manager, message)

# Response length
length = metrics.measure_response_length(response)

# Context utilization
util = metrics.measure_context_utilization(context, response)
```

### Clinical Metrics

Implemented in `evaluation/metrics/clinical_metrics.py`:

```python
from evaluation.metrics import ClinicalMetrics

metrics = ClinicalMetrics(llm)

# Professionalism score (1-5)
prof_score = metrics.evaluate_professionalism(response)

# Empathy score (1-5)
emp_score = metrics.evaluate_empathy(response)

# Safety check
is_safe = metrics.check_safety(response)
```

### Memory Metrics

Implemented in `evaluation/metrics/memory_metrics.py`:

```python
from evaluation.metrics import MemoryMetrics

metrics = MemoryMetrics()

# Memory recall accuracy
accuracy = metrics.evaluate_recall(response, user_history)

# Personalization level
level = metrics.evaluate_personalization(response, user_profile)
```

### RAG Metrics

Implemented in `evaluation/metrics/rag_metrics.py`:

```python
from evaluation.metrics import RAGMetrics

metrics = RAGMetrics()

# Retrieval precision
precision = metrics.evaluate_retrieval_precision(retrieved_docs, query)

# Knowledge utilization
util = metrics.evaluate_knowledge_utilization(retrieved_docs, response)
```

---

## Custom Evaluation

### Define Your Own Test Set

Create `evaluation/datasets/custom_test.json`:

```json
{
  "test_cases": [
    {
      "id": "test_001",
      "user_profile": {
        "age": 25,
        "issues": ["anxiety"]
      },
      "conversation": [
        {"role": "user", "content": "I feel anxious..."}
      ],
      "expected_keywords": ["breathing", "anxiety", "techniques"]
    }
  ]
}
```

### Run Custom Evaluation

```python
from evaluation import SystemEvaluator
from evaluation.datasets import load_custom_dataset

# Load your dataset
dataset = load_custom_dataset('evaluation/datasets/custom_test.json')

# Create evaluator
evaluator = SystemEvaluator(config)

# Evaluate
results = evaluator.evaluate_dataset(dataset)

# Save results
results.save('evaluation/results/custom_eval/')
```

---

## Reproducing Paper Results

### Step 1: Setup

```bash
# Ensure all dependencies installed
pip install -r requirements.txt

# Download required models
bash download_model.sh
```

### Step 2: Run Experiments

```bash
# Comparison experiment (Table 1 in paper)
python examples/comparison_experiment.py

# Case studies (Section 4.2 in paper)
python examples/case_study.py --all
```

### Step 3: Generate Figures

```bash
# Generate all paper figures
python examples/visualize_results.py

# Outputs saved to experiments/figures/
```

### Step 4: View Results

```bash
# Open results
cat experiments/detailed_comparison.md
cat experiments/response_examples.md

# View figures
open experiments/figures/  # macOS
```

---

## Evaluation Best Practices

### 1. Use Consistent Seeds

```python
import random
import numpy as np

random.seed(42)
np.random.seed(42)
```

### 2. Multiple Runs

```bash
# Run experiment 3 times
for i in {1..3}; do
  python examples/comparison_experiment.py --seed $i
done

# Aggregate results
python scripts/aggregate_results.py
```

### 3. Log Everything

```yaml
# Enable detailed logging
logging:
  level: 'DEBUG'
  log_file: 'logs/evaluation.log'
```

### 4. Save Configurations

```python
# Save config with results
results['config'] = config
save_json(results, 'results_with_config.json')
```

---

## Evaluation Datasets

### Built-in Datasets

1. **SmileChat Sample**: `evaluation/datasets/comparison_test_questions.json`
   - 10 carefully selected test cases
   - Covers: anxiety, depression, stress, relationships

2. **Memory Test Set**: Generated by `memory_test_generator.py`
   - Tests multi-session memory capabilities

### External Datasets (Optional)

Download full datasets:

```bash
python evaluation/datasets/download_datasets.py --dataset mentalchat
```

Available datasets:
- MentalChat16K
- Counsel Chat
- Empathetic Dialogues

---

## Automated Evaluation Pipeline

Run complete evaluation pipeline:

```bash
bash scripts/run_full_evaluation.sh
```

This runs:
1. Quick test
2. Comparison experiment
3. Case studies
4. Generate reports and figures

**Estimated time**: 30-60 minutes (depending on LLM backend)

---

## Evaluation Results Format

### JSON Format

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "config": {...},
  "scenarios": [
    {
      "scenario_id": "work_stress_insomnia",
      "configurations": {
        "bare_llm": {
          "metrics": {
            "professionalism": 3.2,
            "personalization": 1.5,
            "empathy": 3.8
          },
          "responses": [...]
        },
        "llm_rag": {...},
        "full_system": {...}
      }
    }
  ],
  "summary": {
    "winner": "full_system",
    "average_improvement": 2.3
  }
}
```

### Markdown Report Format

See `experiments/detailed_comparison.md` for example.

---

## Troubleshooting Evaluation

### Issue: Evaluation Takes Too Long

**Solution 1**: Use faster model
```yaml
llm:
  api:
    model: 'gpt-3.5-turbo'  # Instead of gpt-4
```

**Solution 2**: Reduce test cases
```python
test_cases = test_cases[:5]  # Only first 5
```

### Issue: Out of API Budget

**Solution**: Use local model
```yaml
llm:
  backend: 'local'
```

### Issue: Inconsistent Results

**Solution**: Set random seeds
```python
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
```

---

## Metrics Interpretation

### Professionalism (1-5)

- **5**: Excellent use of evidence-based techniques
- **4**: Good professional guidance
- **3**: Adequate but generic advice
- **2**: Limited professional insight
- **1**: Inappropriate or harmful advice

### Personalization (1-5)

- **5**: Highly personalized, references history
- **4**: Some personalization
- **3**: Neutral, could apply to anyone
- **2**: Ignores user context
- **1**: Contradicts known information

### Empathy (1-5)

- **5**: Deep emotional understanding
- **4**: Warm and supportive
- **3**: Neutral, professional
- **2**: Cold or dismissive
- **1**: Insensitive or judgmental

---

## Further Reading

- [Architecture](architecture.md) - System design
- [Configuration](configuration.md) - Configure evaluation
- [Examples](examples.md) - More code examples

---

**Ready to evaluate?** Start with the quick test, then run the full comparison experiment!
