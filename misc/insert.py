"""Insert random sample values into retention sqilte database."""
from typing import Any, Dict, Set
from sqlalchemy import create_engine, insert, delete, table, column
from sqlalchemy.types import INTEGER, REAL, TEXT
from random import choice
from pprint import pprint
import json


db_path = "sqlite:///../db/retention-sqlite.db"
example_values_path = "../downloads/retention/retention-values.txt"
table_name = "fact_retention_model"
iterations = 100


names = [
    "fathercodename",
    "raisetype",
    "product_type_bi",
    "agencyname_adj",
    "custtype",
    "tougu_flag",
    "business_module",
    "cdate",
    "invest_manager",
    "parentareaname",
    "salescenter",
    "retail_brokername",
    "provname",
    "CITYNAME",
    "relaname",
    "age",
    "port_code",
    "fathercode",
    "fundname",
    "shares",
    "asset",
    "asset_fof"
]
type_mappings = {
    k: TEXT for k in names
}
type_mappings["age"] = INTEGER
type_mappings["shares"] = REAL
type_mappings["asset"] = REAL
type_mappings["asset_fof"] = REAL
values: Dict[str, Set[Any]] = {}


def convert(name, iterable):
    if name in ["shares", "asset", "asset_fof"]:
        return set(map(lambda x: float(x), iterable))
    elif name in ["age"]:
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
        conn.execute(delete(retention_table))

        while iterations > 0:
            # random choice of values from each set
            insert_values = {k: choice(tuple(values[k]))
                             for k in values.keys()}

            stmt = insert(retention_table).values(
                **insert_values)
            # pprint(stmt.compile().params)
            print(
                f"Inserted: {json.dumps(stmt.compile().params, ensure_ascii=False)[:80]}...")
            result = conn.execute(stmt)

            iterations -= 1

        conn.commit()
