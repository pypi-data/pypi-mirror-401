# Polars Lazy API Guide

## IMPORTANT

- VERIFY METHODS EXIST: Before writing code, use `polars_search_api` to confirm method names and `polars_get_docstring` for exact signatures. Polars has its own API—don't assume methods from other libraries exist.
- POLARS IS STRICTLY TYPED: No mixed types, no implicit coercion. Check dtypes with df.schema. Clean data before casting (e.g., replace "N/A" with null), or use .cast(pl.Float64, strict=False) to turn parse failures into nulls.

## Why Use Lazy API

**Always prefer lazy API for better performance.** The lazy API builds a query plan that Polars optimizes before execution.

### Key Benefits

- **Query optimization**: Predicate pushdown, projection pushdown
- **Memory efficiency**: Only loads needed data
- **Parallel execution**: Automatically parallelizes operations
- **Streaming**: Can process larger-than-memory datasets

## Starting a Lazy Query

```python
import polars as pl

# From CSV (lazy scan)
lf = pl.scan_csv("data.csv")

# From Parquet (lazy scan)
lf = pl.scan_parquet("data.parquet")

# From eager DataFrame
df = pl.DataFrame({"a": [1, 2, 3]})
lf = df.lazy()
```

## Basic Operations

All operations return a LazyFrame until `.collect()`:

```python
lf = (
    pl.scan_csv("data.csv")
    .filter(pl.col("age") > 30)
    .select([pl.col("name"), pl.col("salary")])
    .group_by("department")
    .agg(pl.col("salary").mean())
)

# Execute the query
result = lf.collect()
```

## Query Optimization

Polars automatically optimizes:

```python
lf = (
    pl.scan_csv("large_file.csv")
    .select(["col1", "col2", "col3"])  # Projection pushdown
    .filter(pl.col("col1") > 100)      # Predicate pushdown
)

# View query plan
print(lf.explain())
```

**Output shows optimizations applied:**

- Only reads selected columns
- Filters during scan (not after)

## Composition Pattern

Build complex queries step by step:

```python
# Base query
data = pl.scan_csv("data.csv")

base = data.filter(pl.col("status") == "active")

# Add aggregations
result = (
    base
    .group_by("category")
    .agg([
        pl.col("amount").sum().alias("total"),
        pl.col("amount").mean().alias("average")
    ])
    .collect()
)
```
