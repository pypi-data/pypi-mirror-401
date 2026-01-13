# functional_list
**Functional programming for Python lists with Spark RDD-style transformations**

[![Docs](https://img.shields.io/badge/Docs-Netlify-green)](https://functional-list.netlify.app) [![Ray](https://img.shields.io/badge/Backend-Ray-blue)](https://www.ray.io/) [![Dask](https://img.shields.io/badge/Backend-Dask-orange)](https://www.dask.org/) [![Asyncio](https://img.shields.io/badge/Backend-Asyncio-informational)](https://docs.python.org/3/library/asyncio.html) [![PyArrow](https://img.shields.io/badge/IO-PyArrow-6f42c1)](https://arrow.apache.org/docs/python/) [![Pipeline](https://img.shields.io/gitlab/pipeline-status/Tantelitiana22/list-function-python-project?branch=master)](https://gitlab.com/Tantelitiana22/list-function-python-project/-/pipelines) 
[![Coverage](https://img.shields.io/gitlab/coverage/overall/Tantelitiana22/list-function-python-project?branch=master)](https://gitlab.com/Tantelitiana22/list-function-python-project/-/pipelines)
## 🎯 Overview
\`functional_list\` brings functional programming paradigms to Python lists, inspired by Apache Spark RDD operations. It provides both **eager** (\`ListMapper\`) and **lazy** (\`LazyListMapper\`) execution modes, making data transformations more expressive and chainable.
### ✨ Key Features
- **🔗 Functional-style transformations**: \`map\`, \`filter\`, \`reduce\`, \`flat_map\`, \`reduce_by_key\`, and more
- **⚡ Multiple execution backends**:
  - \`Serial\` - Simple sequential execution
  - \`Local\` - Multi-threaded or multi-process parallelization
  - \`Async\` - Asynchronous I/O operations
  - \`Ray\` - Distributed computing with Ray
  - \`Dask\` - Distributed computing with Dask
- **💤 Lazy evaluation**: Build transformation pipelines that execute only when needed
- **📁 File I/O support**: Read from CSV, JSON, JSONL, Parquet, and text files
- **🚀 Cython-accelerated operations**: Optional compiled extensions for performance-critical operations
- **🐍 Fully typed**: Complete type hints for better IDE support and type checking
- **📦 Zero required dependencies**: Install only what you need with optional extras
### 📋 Requirements
- **Python 3.10+** (Python 3.6-3.9 are not supported in recent versions)
## 📦 Installation
### Basic Installation
```bash
pip install functional-list
```
Or using \`uv\`:
```bash
uv add functional-list
```
### Installation with Optional Features
Install with specific backends or I/O support:
```bash
# For Ray distributed computing
pip install functional-list[ray]
# For Dask distributed computing
pip install functional-list[dask]
# For Parquet/CSV file I/O support
pip install functional-list[io]
# Install everything
pip install functional-list[all]
```
With \`uv\`:

```bash
uv add "functional-list[all]"
```

## 🚀 Quick Start
### Basic Usage
```python
from functional_list import ListMapper
# Create a ListMapper
numbers = ListMapper[int](1, 2, 3, 4, 5)
# Chain transformations
result = (
    numbers
    .map(lambda x: x * x)           # [1, 4, 9, 16, 25]
    .filter(lambda x: x % 2 == 0)   # [4, 16]
    .reduce(lambda x, y: x + y)     # 20
)
print(result)  # 20
```
### Word Count Example
The classic MapReduce word count example:
```python
from functional_list import ListMapper
# Given: a list of text documents
document = ListMapper[str](
    "python is good",
    "python is better than x",
    "python is the best",
)
# When: perform word count using functional transformations
word_counts = (
    document
    .flat_map(lambda line: line.split())      # Split into words
    .map(lambda word: (word, 1))              # Create (word, count) pairs
    .reduce_by_key(lambda x, y: x + y)        # Sum counts by word
)
# Then: result is a list of (word, count) tuples
print(word_counts)
# Output: [('than', 1), ('the', 1), ('best', 1), ('better', 1), 
#          ('good', 1), ('is', 3), ('python', 3), ('x', 1)]
```

### Working with Standard List Operations
\`ListMapper\` maintains compatibility with Python's built-in list operations:

```python
from functional_list import ListMapper
my_list = ListMapper[int](2, 4, 9, 13, 15, 20)
# Standard list operations work as expected
my_list.append(55)
print(my_list)  # [2, 4, 9, 13, 15, 20, 55]
# Indexing and slicing
print(my_list[0])     # 2
print(my_list[1:4])   # [4, 9, 13]
# Length
print(len(my_list))   # 7
# Chain functional operations
result = (
    my_list
    .map(lambda x: x * x)
    .filter(lambda x: x % 2 == 0)
    .reduce(lambda x, y: x + y)
)
print(result)  # 3720
```

## 💤 Lazy Evaluation
Use \`LazyListMapper\` for deferred execution - transformations are only computed when needed:

```python
from functional_list import ListMapper
# Convert to lazy mode
lazy_pipeline = (
    ListMapper[int](1, 2, 3, 4, 5)
    .lazy()                              # Switch to lazy evaluation
    .map(lambda x: x * 2)
    .filter(lambda x: x > 5)
    .map(lambda x: x ** 2)
)
# No computation happens yet!
# Materialize the results
result = lazy_pipeline.collect()         # Now computation happens
print(result)  # [36, 64, 100]
# Or iterate (also materializes)
for item in lazy_pipeline:
    print(item)
```

## ⚡ Execution Backends
Choose the right backend for your workload:
### Serial Backend (Default)

```python
from functional_list import ListMapper
data = ListMapper[int](1, 2, 3, 4, 5)
result = data.map(lambda x: x * 2).collect()
```

### Local Backend (Multi-threading/Multi-processing)

```python
from functional_list import ListMapper, LocalBackend
data = ListMapper[int](range(1000))
# Use threading for I/O-bound tasks
result = data.map(
    lambda x: expensive_io_operation(x),
    backend=LocalBackend(use_threads=True, max_workers=10)
).collect()
# Use multiprocessing for CPU-bound tasks
result = data.map(
    lambda x: expensive_cpu_operation(x),
    backend=LocalBackend(use_processes=True, max_workers=4)
).collect()
```

### Async Backend

```python
from functional_list import ListMapper, AsyncBackend
import asyncio
async def async_fetch(url):
    # Your async code here
    pass
data = ListMapper[str](["url1", "url2", "url3"])
result = data.map(async_fetch, backend=AsyncBackend()).collect()
```

### Ray Backend (Distributed Computing)

```python
from functional_list import ListMapper, RayBackend
# Requires: pip install functional-list[ray]
data = ListMapper[int](range(10000))
result = data.map(
    lambda x: complex_computation(x),
    backend=RayBackend(num_cpus=8)
).collect()
```

### Dask Backend (Distributed Computing)

```python
from functional_list import ListMapper, DaskBackend
# Requires: pip install functional-list[dask]
data = ListMapper[int](range(10000))
result = data.map(
    lambda x: complex_computation(x),
    backend=DaskBackend(n_workers=4)
).collect()
```

## 📁 File I/O Operations
\`functional_list\` provides built-in support for reading data from various file formats:
### Supported Formats
| Format | Description | Requires |
|--------|-------------|----------|
| **CSV** | Comma-separated values | Built-in |
| **JSON** | JSON arrays or objects | Built-in |
| **JSONL** | JSON Lines (one object per line) | Built-in |
| **Parquet** | Columnar storage format | \`pyarrow\` |
| **Text** | Plain text files | Built-in |
### Reading CSV Files

```python
from functional_list import ListMapper
from functional_list.io import CSVReadOptions
# Read CSV with custom options
users = ListMapper.from_csv(
    "users.csv",
    options=CSVReadOptions(
        skip_header=True,
        delimiter=",",
        encoding="utf-8"
    ),
    transform=lambda row: {
        "name": row[0],
        "age": int(row[1]),
        "email": row[2]
    }
)
# Process the data
adults = users.filter(lambda user: user["age"] >= 18)
```

### Reading JSON Files

```python
from functional_list import ListMapper
# Read JSON array
data = ListMapper.from_json("data.json")
# Read and transform
names = (
    ListMapper.from_json("users.json")
    .map(lambda user: user["name"])
    .filter(lambda name: len(name) > 3)
)

```

### Reading JSONL Files

```python
from functional_list import ListMapper
# Each line is a separate JSON object
events = ListMapper.from_jsonl("events.jsonl")
# Process streaming logs
errors = (
    events
    .filter(lambda e: e.get("level") == "ERROR")
    .map(lambda e: e["message"])
)
```

### Reading Parquet Files

```python
from functional_list import ListMapper
# Read entire Parquet file
data = ListMapper.from_parquet("data.parquet")
# Read specific columns only
users = ListMapper.from_parquet(
    "users.parquet",
    columns=["name", "age", "country"]
)
# Process efficiently
summary = (
    users
    .filter(lambda u: u["country"] == "USA")
    .map(lambda u: u["age"])
    .reduce(lambda x, y: x + y)
)
```

### Reading Text Files

```python
from functional_list import ListMapper
from functional_list.io import TextReadOptions
# Read with options
lines = ListMapper.from_text(
    "log.txt",
    options=TextReadOptions(
        strip_lines=True,      # Remove whitespace
        skip_empty=True,       # Skip empty lines
        encoding="utf-8"
    )
)
# Process log file
error_lines = (
    lines
    .filter(lambda line: "ERROR" in line)
    .map(lambda line: line.split("|"))
)
```

## 📚 Core API Reference

### Transformation Methods

| Method | Description | Example |
|--------|-------------|---------|
| \`map(fn)\` | Apply function to each element | \`data.map(lambda x: x * 2)\` |
| \`filter(fn)\` | Keep elements where fn returns True | \`data.filter(lambda x: x > 0)\` |
| \`flat_map(fn)\` | Map and flatten results | \`data.flat_map(lambda x: [x, x*2])\` |
| \`reduce(fn)\` | Reduce to single value | \`data.reduce(lambda x, y: x + y)\` |
| \`reduce_by_key(fn)\` | Reduce grouped by key | \`pairs.reduce_by_key(lambda x, y: x + y)\` |
| \`group_by(fn)\` | Group elements by key function | \`data.group_by(lambda x: x % 2)\` |
| \`group_by(fn)\` | Group elements by key function | \`data.group_by(lambda x: x % 2)\` |
| \`sort(key, reverse)\` | Sort elements with optional key function | \`data.sort(key=lambda x: x["age"])\` |
| \`distinct()\` | Remove duplicates | \`data.distinct()\` |
| \`union(other)\` | Combine two ListMappers (type-safe) | \`list1.union(list2)\` |
| \`take(n)\` | Take first n elements | \`data.take(10)\` |
| \`sample(n)\` | Random sample of n elements | \`data.sample(5)\` |

### Aggregation Methods

| Method | Description | Example |
|--------|-------------|---------|
| \`count()\` | Count elements | \`data.count()\` |
| \`sum()\` | Sum numeric elements | \`data.sum()\` |
| \`mean()\` | Calculate mean | \`data.mean()\` |
| \`min()\` | Find minimum | \`data.min()\` |
| \`max()\` | Find maximum | \`data.max()\` |
| \`collect()\` | Materialize to list | \`lazy_data.collect()\` |
## 🎓 Advanced Examples
### Processing Log Files

```python
from functional_list import ListMapper
from datetime import datetime
# Parse and analyze log files
errors_by_hour = (
    ListMapper.from_text("app.log")
    .filter(lambda line: "ERROR" in line)
    .map(lambda line: line.split("|"))
    .map(lambda parts: {
        "timestamp": datetime.fromisoformat(parts[0]),
        "message": parts[2]
    })
    .map(lambda e: (e["timestamp"].hour, 1))
    .reduce_by_key(lambda x, y: x + y)
    .sort(key=lambda x: x[1], reverse=True)
)
```

### ETL Pipeline

```python
from functional_list import ListMapper
# Load from multiple sources
csv_users = ListMapper.from_csv("users.csv", transform=parse_user)
json_users = ListMapper.from_json("new_users.json")
# Combine and process
all_users = (
    csv_users
    .union(json_users)
    .distinct()
    .filter(lambda u: u["active"])
    .map(lambda u: enrich_user(u))
)
# Save results
all_users.to_json("processed_users.json")
```

### Parallel Web Scraping

```python
from functional_list import ListMapper, LocalBackend
import requests
def fetch_page(url):
    return requests.get(url).text
urls = ListMapper[str](
    "https://example.com/page1",
    "https://example.com/page2",
)
# Fetch pages in parallel
pages = urls.map(
    fetch_page,
    backend=LocalBackend(use_threads=True, max_workers=10)
)
# Extract data
results = pages.map(parse_html).flat_map(extract_links).distinct()
```

## 🔧 Performance Tips
1. **Choose the right backend**: Use \`LocalBackend\` with threads for I/O-bound tasks, processes for CPU-bound
2. **Use lazy evaluation**: Build pipelines with \`.lazy()\` to optimize execution
3. **Cache intermediate results**: Use \`.cache()\` on expensive computations
4. **Batch operations**: Combine multiple transformations before materializing
5. **Use Cython accelerators**: Ensure extensions are compiled for numerical operations
## 🤝 Contributing
Contributions are welcome! Please check out our [GitLab repository](https://gitlab.com/Tantelitiana22/list-function-python-project).
### Development Setup

```bash
# Clone the repository
git clone https://gitlab.com/Tantelitiana22/list-function-python-project.git
cd list-function-python-project
# Install with development dependencies
uv sync --group dev --extra all
# Run tests
uv run pytest
# Run type checking
uv run mypy ./src/functional_list/
# Run linters
uv run flake8 ./src/functional_list/
uv run pylint ./src/functional_list/
```

## 📖 Documentation
### Full Documentation (MkDocs)
Complete documentation is available at [https://sensational-cobbler-2b96f1.netlify.app/](https://sensational-cobbler-2b96f1.netlify.app/)
To run documentation locally:

```bash
uv sync --group dev
mkdocs serve -f documentation/mkdocs.yml
```
### Quick API Reference

```python
from functional_list import ListMapper
# List all methods
print(dir(ListMapper))
# Get documentation for a specific method
print(ListMapper.map.__doc__)
# Get help
help(ListMapper.reduce_by_key)
```

## ❓ FAQ & Troubleshooting
### Why am I getting "module not found" errors for Ray/Dask?
You need to install the optional dependencies:
```bash
pip install functional-list[ray]  # For Ray
pip install functional-list[dask]  # For Dask
pip install functional-list[all]   # For everything
```
### Can I use this with Python 3.9 or earlier?
No, \`functional_list\` requires **Python 3.10+**. Earlier versions are not supported.
### How do I improve performance for large datasets?
1. Use lazy evaluation: \`.lazy()\` to defer execution
2. Choose appropriate backends (Ray/Dask for distributed computing)
3. Use \`.cache()\` for intermediate results you'll reuse
4. Ensure Cython extensions are compiled
### Does this work with async functions?
Yes! Use the \`AsyncBackend\`:
```python
from functional_list import ListMapper, AsyncBackend
async def async_operation(x):
    # Your async code
    pass
result = data.map(async_operation, backend=AsyncBackend())
```
## 📄 License
This project is licensed under the terms specified in the LICENSE file.
## 👤 Author
**Andrianarivo Tantelitiana RAKOTOARIJAONA**
- Email: tantelitiana22@gmail.com
- GitLab: [Tantelitiana22](https://gitlab.com/Tantelitiana22)
## 🔗 Links
- [Documentation](https://sensational-cobbler-2b96f1.netlify.app/)
- [GitLab Repository](https://gitlab.com/Tantelitiana22/list-function-python-project)
- [PyPI Package](https://pypi.org/project/functional-list/)
---
**⭐ If you find this library useful, please consider giving it a star on GitLab!**
