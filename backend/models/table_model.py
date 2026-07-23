from pydantic import BaseModel
from typing import List


class Column(BaseModel):
    name: str
    datatype: str
    nullable: bool = True


class ForeignKey(BaseModel):
    column: str
    reference_table: str
    reference_column: str


class Table(BaseModel):
    table_name: str
    columns: List[Column] = []
    primary_keys: List[str] = []
    foreign_keys: List[ForeignKey] = []