from pyspark.sql.functions import explode_outer, col
from pyspark.sql.types import StructType, ArrayType


def flatten_recursive(df):
    """
    Recursively flattens all StructType and ArrayType columns
    in a PySpark DataFrame.

    - Structs are expanded into individual columns
    - Arrays are exploded using explode_outer
    - Continues until no complex types remain

    Parameters
    ----------
    df : pyspark.sql.DataFrame

    Returns
    -------
    pyspark.sql.DataFrame
    """

    def has_complex_types(schema):
        return any(
            isinstance(field.dataType, (StructType, ArrayType))
            for field in schema.fields
        )

    while has_complex_types(df.schema):
        for field in df.schema.fields:
            name = field.name
            dtype = field.dataType

            if isinstance(dtype, StructType):
                expanded_cols = [
                    col(f"{name}.{f.name}").alias(f"{name}_{f.name}")
                    for f in dtype.fields
                ]
                df = df.select("*", *expanded_cols).drop(name)

            elif isinstance(dtype, ArrayType):
                df = df.withColumn(name, explode_outer(col(name)))

    return df
