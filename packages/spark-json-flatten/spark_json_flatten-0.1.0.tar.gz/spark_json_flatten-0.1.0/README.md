# spark-json-flatten

A lightweight utility to **recursively flatten complex PySpark DataFrames**
containing deeply nested structs and arrays.

## Features
- Recursive schema flattening
- Handles arbitrary nesting depth
- Uses `explode_outer` for safe array expansion
- No UDFs, fully Spark-native

## Installation
```bash
pip install spark-json-flatten

from spark_json_flatten import flatten_recursive

flattened_df = flatten_recursive(complex_df)
