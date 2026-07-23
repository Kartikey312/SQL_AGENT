from pydantic import BaseModel, Field
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
    columns: List[Column] = Field(default_factory=list)
    primary_keys: List[str] = Field(default_factory=list)
    foreign_keys: List[ForeignKey] = Field(default_factory=list)