import time


def escape_string(str):
    return "".join(
        [
            c
            for c in str
            if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -()/_"
        ]
    )


def is_safe(str):
    return str == escape_string(str)


def slugify(text):
    return escape_string(
        text.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("(", "_")
        .replace(")", "_")
        .replace("/", "_")
        .replace("___", "_")
        .replace("__", "_")
        .strip("_")
    )


def remove_new_lines_from_string(text):
    return text.replace("\n", "").replace("\r", "").strip()


def dump_sql_to_rows(cursor, sql, debug=False):
    start_time = time.time()
    cursor.execute(sql)
    end_time = time.time()
    duration = end_time - start_time
    if debug:
        print(f"[pyodbc-extras] executing SQL took {duration:.4f} seconds to run")
    column_names = [column[0] for column in cursor.description]
    rows = [dict(zip(column_names, row)) for row in cursor]
    return {"column_names": column_names, "rows": rows}


def dump_table(cursor, table_name):
    if not is_safe(table_name):
        raise Exception("[pyodbc-extras] table name is not safe")
    return dump_sql_to_rows(cursor, f"SELECT * FROM {table_name}")
