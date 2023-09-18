"""Insert random sample values into retention sqilte database."""
from typing import Any, Dict, Set
from sqlalchemy import create_engine, insert, table, column, text
from sqlalchemy.types import INTEGER, REAL, TEXT
from random import choice
import json


db_path = "sqlite:///../db/retention-sqlite.db"
create_sql_file = "retention/create.sql"
example_values_path = "retention/values.txt"
table_name = "fact_retention_model"
iterations = 1000


names = [
    "fathercodename",
    "raisetype",
    "product_type_bi",
    "agencyname",
    "property",
    "is_settlement",
    "custtype",
    "tougu_flag",
    "business_module",
    "cdate",
    "islastwkday_month",
    "islastwkday_quarter",
    "islastwkday_year",
    "invest_manager",
    "parentareaname",
    "salescenter",
    "retail_brokername",
    "province",
    "city",
    "relaname",
    "age",
    "port_code",
    "fathercode",
    "fundname",
    "shares",
    "asset",
    "asset_fof",
    "customer_id"
]
type_mappings = {
    k: TEXT for k in names
}
type_mappings["age"] = INTEGER
type_mappings["shares"] = REAL
type_mappings["asset"] = REAL
type_mappings["asset_fof"] = REAL
type_mappings["customer_id"] = INTEGER
values: Dict[str, Set[Any]] = {}


def convert(name, iterable):
    if name in ["shares", "asset", "asset_fof"]:
        return set(map(lambda x: float(x), iterable))
    elif name in ["age", "customer_id"]:
        return set(map(lambda x: int(x), iterable))
    else:
        return iterable


with open(example_values_path, "r") as file:
    for i, line in enumerate(file):
        entries = line.split(",")
        stripped = set(map(lambda s: s.strip().strip("'"), entries))
        values[names[i]] = convert(names[i], stripped)

    engine = create_engine(db_path)
    columns = tuple(list(map(lambda n: column(n, type_mappings[n]), names)))
    retention_table = table(
        table_name,
        *columns
    )

    with engine.connect() as conn:
        with open(create_sql_file, "r") as create:
            query = text(create.read())
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
            conn.execute(query)

        n = iterations
        while n > 0:
            # random choice of values from each set
            insert_values = {k: choice(tuple(values[k]))
                             for k in values.keys()}

            stmt = insert(retention_table).values(
                **insert_values)
            # pprint(stmt.compile().params)
            print(
                f"Inserted: {json.dumps(stmt.compile().params, ensure_ascii=False)[:80]}...")
            result = conn.execute(stmt)

            n -= 1

        conn.commit()

    print(f"{iterations} entries inserted into table {table_name}")
