from sqlglot import expressions as exp
from models.table_model import Table, Column, ForeignKey


def extract_tables(expressions):
    tables = []

    for expression in expressions:

        if not isinstance(expression, exp.Create):
            continue

        schema = expression.find(exp.Schema)

        if not schema:
            continue

        table = Table(table_name=schema.this.name)

        for item in schema.expressions:

            # ----------------------------
            # Column
            # ----------------------------
            if isinstance(item, exp.ColumnDef):

                column = Column(
                    name=item.name,
                    datatype=item.args["kind"].sql()
                )

                # Check column constraints
                for constraint in item.args.get("constraints", []):

                    if isinstance(constraint.kind, exp.PrimaryKeyColumnConstraint):
                        table.primary_keys.append(column.name)

                table.columns.append(column)

            # ----------------------------
            # Foreign Key
            # ----------------------------
            elif isinstance(item, exp.ForeignKey):

                fk_column = item.expressions[0].name

                ref_schema = item.args["reference"].this

                ref_table = ref_schema.this.name
                ref_column = ref_schema.expressions[0].name

                table.foreign_keys.append(
                    ForeignKey(
                        column=fk_column,
                        reference_table=ref_table,
                        reference_column=ref_column
                    )
                )

        tables.append(table)

    return tables