from parser.sql_parser import parse_sql
from parser.table_parser import extract_tables

with open("uploads/customer.sql") as f:
    sql = f.read()

expressions = parse_sql(sql)

tables = extract_tables(expressions)

for table in tables:

    print("=" * 50)
    print(f"Table : {table.table_name}")

    print("\nColumns")

    for c in table.columns:
        print(f"  {c.name:15} {c.datatype}")

    print("\nPrimary Keys")

    for pk in table.primary_keys:
        print(f"  {pk}")

    print("\nForeign Keys")

    if table.foreign_keys:
        for fk in table.foreign_keys:
            print(
                f"  {fk.column} --> "
                f"{fk.reference_table}.{fk.reference_column}"
            )
    else:
        print("  None")

    print("=" * 50)