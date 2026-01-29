"""Equinox task prompt - guides LLM on Equinox development."""

EQUINOX_TASK_PROMPT = """
# Equinox Development Guide

When working with Equinox, follow these guidelines:

## Tools Available

1. **list-sections**: Discover available documentation sections
2. **get-documentation**: Fetch specific documentation content
3. **equinox-checker**: Validate your generated Equinox module code

## Workflow

1. Use `list-sections` first to see what documentation is available
2. Use `equinox-checker` to validate code BEFORE presenting to user
3. Use `get-documentation` for specific API details when needed

## Key Equinox Patterns

### Module Definition

```python
import equinox as eqx
import jax.numpy as jnp
from jax import Array
from jax.typing import ArrayLike
from dataclasses import field

class MyModule(eqx.Module):
    # Learnable parameters (included in PyTree)
    weight: Array
    bias: Array

    # Static hyperparameters (excluded from PyTree)
    num_heads: int = field(static=True)
    hidden_size: int = field(static=True)

    def __init__(
        self,
        in_features: int,
        out_features: int,
        *,
        key: PRNGKeyArray,  # Explicit randomness
    ):
        self.num_heads = 8
        self.hidden_size = out_features
        self.weight = jax.random.normal(key, (out_features, in_features))
        self.bias = jnp.zeros(out_features)

    def __call__(
        self,
        x: ArrayLike,  # [seq, in_features] - no batch dimension!
        *,
        key: Optional[PRNGKeyArray] = None,  # For dropout
    ) -> Array:  # [seq, out_features]
        return x @ self.weight.T + self.bias
```

### Critical Rules

1. **No batch dimension in __call__**: Use `jax.vmap` for batching
   ```python
   # Correct: vmap for batching
   batched_output = jax.vmap(model)(batched_input)
   ```

2. **Explicit PRNG keys**: Always pass keys explicitly
   ```python
   key1, key2 = jax.random.split(key)
   layer1 = MyLayer(key=key1)
   layer2 = MyLayer(key=key2)
   ```

3. **Static fields for hyperparameters**: Non-JAX types need `field(static=True)`
   ```python
   num_layers: int = field(static=True)  # Not a JAX array
   ```

4. **Shape annotations**: Document tensor shapes in comments
   ```python
   # [batch, seq, dim] @ [dim, hidden] -> [batch, seq, hidden]
   h = x @ self.weight
   ```

5. **PyTree compatibility**: All fields must be valid JAX types or marked static

## Common Mistakes to Avoid

- Mutable default arguments (use `field(default_factory=list)`)
- Forgetting `field(static=True)` for int/str/bool fields
- Including batch dimension in module's `__call__`
- Not passing PRNG keys through the call stack
"""