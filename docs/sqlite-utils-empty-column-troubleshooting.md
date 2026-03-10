# sqlite-utils `--schema` and empty CSV text columns

When a CSV column is entirely empty (`""`/missing values for every row), SQLite type inference may classify that column as `INTEGER` when using `sqlite-utils memory <file.csv> --schema`.

Example input:

```csv
id,name
1,
2,
```

Potential output:

```sql
CREATE TABLE "empty_names" (
   "id" INTEGER,
   "name" INTEGER
);
```

## Why this happens

Type inference relies on sampled values. If a column never contains a non-empty string value, there is no evidence that the column should be `TEXT`, so it can fall back to a numeric/`INTEGER` affinity.

## Practical workarounds

- Seed at least one non-empty value in that column before inferring schema.
- Create the table with an explicit schema (`name TEXT`) and import into it.
- Post-process generated DDL and coerce selected columns to `TEXT` when your domain requires textual affinity.

## Regression harness snippet

```python
import pathlib
from click.testing import CliRunner
from sqlite_utils import cli

runner = CliRunner()

with runner.isolated_filesystem():
    tmp = pathlib.Path(".")
    empty_csv = tmp / "empty_names.csv"
    empty_csv.write_text("id,name\n1,\n2,\n", "utf-8")

    result = runner.invoke(
        cli.cli,
        ["memory", str(empty_csv), "--schema"],
        catch_exceptions=False,
    )
    print(result.output)
```
