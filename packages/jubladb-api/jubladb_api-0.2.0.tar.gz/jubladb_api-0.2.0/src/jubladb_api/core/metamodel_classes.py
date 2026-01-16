import dataclasses
import enum

class _EnumReprHelper(object):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

class Operation(_EnumReprHelper, enum.Enum):
    GetList = "GetList"
    GetSingle = "GetSingle"
    CreateSingle = "CreateSingle"
    UpdateSingle = "UpdateSingle"
    DeleteSingle = "DeleteSingle"



class AttributeType(_EnumReprHelper, enum.Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    BOOLEAN = "boolean"

@dataclasses.dataclass
class RelationType(object):
    relation_name: str
    related_type_singular: str
    related_type_plural: str
    to_many: bool

@dataclasses.dataclass
class Attribute:
    name: str
    type_: AttributeType
    array: bool = False
    optional: bool = False
    sortable: bool = False
    filter_name: str|None = None
    filter_types: list[str] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class Entity:
    url: str
    name_singular: str
    name_plural: str
    allowed_operations: list[Operation] = dataclasses.field(default_factory=list)
    attributes: list[Attribute] = dataclasses.field(default_factory=list)
    relations: list[RelationType] = dataclasses.field(default_factory=list)
    includeable: list[str] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class APIInfo(object):
    version: str
    auth_header: str
    default_server_url: str