# Local Cloud Mirror Training

This script replicates the exact training execution flow from the Konic Cloud Platform's
train container for local development and testing.

## Cloud Platform Flow Replicated

1. Load agent from file path (mimics downloading from presigned S3 URL)
2. Detect agent type (finetuning vs traditional RL)
3. Initialize engine from agent configuration
4. Run training with iteration logging
5. Save checkpoints and final model
6. Optional: Log metrics to MLflow

## Usage

### Basic Usage

```bash
# Run with CLI arguments
python run_training.py --agent-path ../basic/sentiment_rlhf.py --iterations 10

# Run with environment variables (cloud-style)
AGENT_PATH=../basic/sentiment_rlhf.py ITERATIONS=10 python run_training.py
```

### With MLflow Tracking

```bash
# Enable MLflow logging
python run_training.py --agent-path ./agent.py --use-mlflow

# Custom MLflow URI
python run_training.py --agent-path ./agent.py --use-mlflow --mlflow-uri http://localhost:5000
```

### With Checkpoints

```bash
# Save checkpoint every 10 iterations
python run_training.py --agent-path ./agent.py --checkpoint-interval 10 --checkpoint-dir ./my_checkpoints
```

## Environment Variables

| Variable            | Default        | Description                          |
| ------------------- | -------------- | ------------------------------------ |
| AGENT_PATH          | -              | Path to agent.py file (required)     |
| ITERATIONS          | 100            | Number of training iterations        |
| CHECKPOINT_INTERVAL | 0              | Save every N iterations, 0=final     |
| CHECKPOINT_DIR      | ./checkpoints  | Where to save model checkpoints      |
| USE_MLFLOW          | false          | Enable MLflow tracking               |
| MLFLOW_TRACKING_URI | ./mlruns       | MLflow server URI                    |

## Requirements

```bash
pip install konic[finetuning]

# Optional: for MLflow tracking
pip install mlflow
```
