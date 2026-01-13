# Easy Map Reduce for a list python:

[![Docs](https://img.shields.io/badge/Docs-Netlify-green)](https://sensational-cobbler-2b96f1.netlify.app/) \
[![Ray](https://img.shields.io/badge/Backend-Ray-blue)](https://www.ray.io/) \
[![Dask](https://img.shields.io/badge/Backend-Dask-orange)](https://www.dask.org/) \
[![Asyncio](https://img.shields.io/badge/Backend-Asyncio-informational)](https://docs.python.org/3/library/asyncio.html) \
[![PyArrow](https://img.shields.io/badge/IO-PyArrow-6f42c1)](https://arrow.apache.org/docs/python/) \
[![Pipeline](https://img.shields.io/gitlab/pipeline-status/Tantelitiana22/list-function-python-project?branch=master)](https://gitlab.com/Tantelitiana22/list-function-python-project/-/pipelines) \
[![Coverage](https://img.shields.io/gitlab/coverage/overall/Tantelitiana22/list-function-python-project?branch=master)](https://gitlab.com/Tantelitiana22/list-function-python-project/-/pipelines)

## Description
This library was created to allow us to use functional style in a list object
in python. It is easier to use functional style when we have for example to deal with a several 
transformation in our data. 

In this little library, we can find most of the function used in a list object but with map
or reduce or flatten,... methods. If you are familiar with spark rdd,
the behavior of all the methods  created in ListMapper object is mostly the same. The difference is that it includes some properties of a python list.

## News
Now a doc-string was added to this package, so you can use it 
and have some example of how to use a method in the object
created with ListMapper

## Issues:
This Library work only with __python version >=3.6__.
If you attempt to use it with an anterior version, there will be
an error occurred in some methods.

## How to use this package:
First install this package with pip by doing:
```
pip install functional-list
```
Then, you can import ListMapper to create an object:
```
from functional_list import ListMapper
``` 
## Example:
Let's make the famous word count with this package.
Suppose one have a list of a document comes from a text file, 
and we load it in a simple list
```
document =[
            "python is good",
            "python is better than x",
            "python is the best",
            ]

## Now, let tranform the list to a list mapper 
document = ListMapper[str](*document)

res = document.flat_map(lambda x:x.split())\
              .map(lambda x:(x,1))\
              .reduce_by_key(lambda x,y:x+y)

## result will be:
#List[('than', 1), ('the', 1), ('best', 1),
#        ('better', 1), ('good', 1), ('is', 3), 
#        ('python', 3), ('x', 1)]
# And you have your word count :)
```
The ListMapper object has also the same behavior as a standard
python list.
```
my_list = ListMapper[int](2, 4, 9, 13, 15, 20)
## Append element 
my_list.append(55)
## will give List[2, 4, 9, 13, 15, 20, 55]
## Let make some ordianry transformation
my_list.map(lambda x: x*x)\
       .filter(lambda x:x%2==0)\
       .reduce(lambda x,y:x+y)

# Give as a result 420

```

## I/O Operations

ListMapper now supports reading data directly from various file formats:

### Supported Formats
- **CSV** - Comma-separated values files
- **JSON** - JSON files (arrays or single objects)
- **JSONL** - JSON Lines format (one JSON object per line)
- **Parquet** - Parquet files (requires `pyarrow`)
- **Text** - Plain text files (one line per element)

### Quick Examples

```python
from functional_list import ListMapper
from functional_list.io import CSVReadOptions, TextReadOptions

# Read CSV and process
users = (
    ListMapper.from_csv(
        "users.csv",
        options=CSVReadOptions(skip_header=True),
        transform=lambda row: {"name": row[0], "age": int(row[1])},
    )
    .filter(lambda user: user["age"] >= 18)
)

# Read JSON and transform
names = ListMapper.from_json("data.json").map(lambda x: x["name"])

# Read text file
lines = ListMapper.from_text(
    "log.txt",
    options=TextReadOptions(strip_lines=True, skip_empty=True),
)

# Read Parquet with specific columns
rows = ListMapper.from_parquet("data.parquet", columns=["name", "age"])

# Read JSONL (JSON Lines)
events = ListMapper.from_jsonl("events.jsonl")
```

### Installation for Parquet Support

```bash
# For Parquet support:
uv add pyarrow
# or
pip install pyarrow
```

For more details, see the MkDocs documentation in `documentation/`.

## Documentation (MkDocs)

La documentation MkDocs est disponible dans le dossier `documentation/`.

Pour la lancer en local:

```bash
uv sync
mkdocs serve -f documentation/mkdocs.yml
```

Pour builder le site:

```bash
mkdocs build -f documentation/mkdocs.yml
```

## Deploy documentation (GitLab CI → Netlify)

This repository includes a GitLab CI pipeline that builds MkDocs from `documentation/mkdocs.yml` and deploys the generated static site to Netlify.

See: `documentation/NETLIFY_GITLAB.md`

## Getting Help

If you want to get the list of the method in this object,
you just have to do the next command in python:
```
dir(ListMapper)
```
To get the doc-string of a method:
```
print(my_list.map.__doc__)
```
In each, method, there is an example of how to use the method.
