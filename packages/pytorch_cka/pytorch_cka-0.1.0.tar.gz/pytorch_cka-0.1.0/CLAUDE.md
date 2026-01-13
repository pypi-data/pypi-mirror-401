# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Development Commands

```bash
# Install dependencies (using uv)
uv sync

# Install with dev dependencies
uv sync --all-extras

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_cka.py

# Run a specific test
uv run pytest tests/test_cka.py::TestCKAClass::test_same_model_comparison

# Run tests with coverage
uv run pytest --cov=pytorch_cka

# Format code
uv run black pytorch_cka tests
uv run isort pytorch_cka tests

# Type checking
uv run mypy pytorch_cka

# Lint
uv run ruff check pytorch_cka
```

## Architecture Overview

This library implements Centered Kernel Alignment (CKA) for comparing neural network representations using minibatch HSIC accumulation.

### Core Modules

- **`pytorch_cka/core.py`**: Mathematical primitives
  - `hsic()`: Unbiased HSIC estimator (requires batch size > 3)
  - `compute_gram_matrix()`: Linear kernel Gram matrix (K = X @ X^T)
  - `EPSILON`: Numerical stability constant (1e-6)

- **`pytorch_cka/cka.py`**: Main `CKA` class
  - Context manager pattern for safe forward hook lifecycle
  - Supports both single-model self-comparison and two-model comparison
  - Same-model optimization: single forward pass when `model1 is model2`
  - Symmetric optimization: computes upper triangle only when layers match
  - Auto-unwraps DataParallel/DDP models
  - Accumulates HSIC values per-batch (memory-efficient minibatch CKA)

- **`pytorch_cka/utils.py`**: Utilities
  - `FeatureCache`: Stores layer outputs with optional detach
  - `validate_batch_size()`: Ensures n > 3 for unbiased HSIC
  - `unwrap_model()`: Handles DataParallel/DDP wrappers
  - `get_device()`: Device detection from model parameters

- **`pytorch_cka/viz.py`**: Visualization functions
  - All functions return `(Figure, Axes)` tuples for customization
  - `plot_cka_heatmap()`, `plot_cka_trend()`, `plot_cka_comparison()`

### Key Design Patterns

1. **Hook Management**: The CKA class uses Python's context manager protocol (`__enter__`/`__exit__`) to ensure forward hooks are always cleaned up, even on exceptions.

2. **Minibatch CKA**: Instead of storing all activations, HSIC values are accumulated per-batch using the formula:
   ```
   CKA = sum(HSIC_xy) / sqrt(sum(HSIC_xx) * sum(HSIC_yy))
   ```

3. **Feature Extraction**: Hooks handle various output formats:
   - Plain tensors
   - Tuple outputs (e.g., attention layers) - uses first element
   - HuggingFace `ModelOutput` objects - extracts `last_hidden_state`

### Test Organization

Tests are in `tests/` with shared fixtures in `conftest.py` and helpers in `helpers.py`:
- `test_cka.py`: Core CKA functionality
- `test_core.py`: HSIC and Gram matrix tests
- `test_viz.py`: Visualization tests
- `test_torchvision_models.py`, `test_timm_models.py`, `test_huggingface_models.py`: Integration tests with real models

Test constants (in `helpers.py`):
- `TEST_BATCH_SIZE = 16` (must be > 3 for unbiased HSIC)
- `TEST_NUM_SAMPLES = 32` (2 batches for CI speed)
