# pyodbc-extras
> Extra Methods for Working with ODBC Connections in Python

## install
```sh
pip install pyodbc-extras
```

## usage
```python
from pyodbc import connect

from pyodbc_extras import dump_sql_to_rows, dump_table

cnxn = pyodbc.connect(CONNECTION_STRING)
cursor = cnxn.cursor()

# dump custom sql
dump_sql_to_rows(cursor, "SELECT * FROM cars WHERE year < 2015")
{ "column_names": ["year", "make", "model", ...], "rows": [{"year": 2005, "make": "Audi", "model": "A3"}, ...] }

# same as dump_sql_to_rows(cursor, "SELECT * FROM cars") 
rows = dump_table(cursor, "cars")
```
