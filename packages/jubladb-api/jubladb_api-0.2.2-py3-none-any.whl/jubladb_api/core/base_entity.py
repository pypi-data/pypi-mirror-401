import datetime
import typing

import jubladb_api.core.metamodel_classes
import abc

class EntityJsonParsingError(Exception):
    pass

class BaseEntity(abc.ABC):
    def __init__(self, id_: int):
        self._id = id_

    @property
    def id(self) -> int:
        return self._id

    @property
    @abc.abstractmethod
    def key(self) -> "BaseEntityKey":
        pass

    @property
    @abc.abstractmethod
    def meta(self) -> jubladb_api.core.metamodel_classes.Entity:
        pass

    @abc.abstractmethod
    def is_relation_loaded(self, relation_name: str) -> bool:
        pass

    @classmethod
    @abc.abstractmethod
    def from_json(cls, json_dict: dict):
        pass

    @classmethod
    def _access_json_single_relation_id(cls, json_data: dict, relation_name: str, related_type_name_plural: str) -> int | None:
        json_relationship = json_data["relationships"][relation_name]
        if "data" not in json_relationship:
            json_meta = json_relationship.get("meta", {})
            if not json_meta.get("included", False):
                return None
            else:
                raise ValueError(f"Expected relation {related_type_name_plural} to either have data or included: false")
        json_relation_data = json_relationship["data"]
        if json_relation_data["type"] != related_type_name_plural:
            raise ValueError(f"Expected relation {related_type_name_plural}, got {json_relation_data['type']}")
        return int(json_relation_data["id"])

    @classmethod
    def _create_single_relation_key(cls, json_data: dict, relation_name: str, related_type_name_plural: str, key_class):
        relation_id = cls._access_json_single_relation_id(json_data, relation_name, related_type_name_plural)
        return key_class(relation_id) if relation_id is not None else None

    @classmethod
    def _access_json_many_relation_ids(cls, json_data: dict, relation_name: str, related_type_name_plural: str) -> list[int] | None:
        json_relationship = json_data["relationships"][relation_name]
        if "data" not in json_relationship:
            json_meta = json_relationship.get("meta", {})
            if not json_meta.get("included", False):
                return None
            else:
                raise ValueError(f"Expected relation {related_type_name_plural} to either have data or included: false")
        res: list[int] = []
        for json_relation_data in json_relationship["data"]:
            if json_relation_data["type"] != related_type_name_plural:
                raise ValueError(f"Expected relation {related_type_name_plural}, got {json_relation_data['type']}")
            res.append(int(json_relation_data["id"]))
        return res

    @classmethod
    def _create_many_relation_keys(cls, json_data: dict, relation_name: str, related_type_name_plural: str, key_class):
        relation_ids = cls._access_json_many_relation_ids(json_data, relation_name, related_type_name_plural)
        return [key_class(rid) for rid in relation_ids] if relation_ids is not None else None

    @classmethod
    def _access_id(cls, json_data: dict) -> int:
        try:
            raw_id = json_data["id"]
        except KeyError:
            raise EntityJsonParsingError("no \"id\" attribute in data object")
        try:
            return int(raw_id)
        except TypeError:
            raise EntityJsonParsingError(f"cannot parse id of data object, value is {repr(raw_id)}")

    @classmethod
    def _access_data_attribute(cls, json_data: dict, attribute_name: str, attribute_type: jubladb_api.core.metamodel_classes.AttributeType, optional: bool=False, array: bool=False) -> typing.Any:
        try:
            attributes = json_data["attributes"]
        except KeyError:
            raise EntityJsonParsingError("no \"attributes\" attribute in data object")
        try:
            raw_value = attributes[attribute_name]
        except KeyError:
            if optional:
                raw_value = None
            else:
                raise EntityJsonParsingError(f"no attribute \"{attribute_name}\" found in json_data[\"attributes\"]")

        if raw_value is None:
            if optional:
                return None
            else:
                raise EntityJsonParsingError(f"value of attribute \"{attribute_name}\" is None, but not marked as optional")

        if array != isinstance(raw_value, list):
            raise EntityJsonParsingError(f"attribute \"{attribute_name}\" should be an array, but is not (or vice versa)")

        def _parse_attribute_value(value: typing.Any) -> typing.Any:
            try:
                if attribute_type == jubladb_api.core.metamodel_classes.AttributeType.STRING:
                    return str(value)
                elif attribute_type == jubladb_api.core.metamodel_classes.AttributeType.INTEGER:
                    return int(value)
                elif attribute_type == jubladb_api.core.metamodel_classes.AttributeType.FLOAT:
                    return float(value)
                elif attribute_type == jubladb_api.core.metamodel_classes.AttributeType.DATE:
                    return datetime.date.fromisoformat(value)
                elif attribute_type == jubladb_api.core.metamodel_classes.AttributeType.TIME:
                    return datetime.time.fromisoformat(value)
                elif attribute_type == jubladb_api.core.metamodel_classes.AttributeType.DATETIME:
                    return datetime.datetime.fromisoformat(value)
                elif attribute_type == jubladb_api.core.metamodel_classes.AttributeType.BOOLEAN:
                    return str(value).lower() == "true" or str(value).lower() == "1"
                else:
                    raise EntityJsonParsingError(f"cannot parse attribute {attribute_name}: unsupported attribute type {attribute_type}")
            except Exception as e:
                raise EntityJsonParsingError(f"cannot parse or convert attribute {attribute_name}: {e}")

        if array:
            return [_parse_attribute_value(rv) for rv in raw_value]
        else:
            return _parse_attribute_value(raw_value)


    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"


class BaseEntityKey(abc.ABC):
    def __init__(self, id_: int):
        self._id = id_

    @property
    @abc.abstractmethod
    def type(self) -> str:
        pass

    @property
    def id(self) -> int:
        return self._id

    def __hash__(self):
        return hash(self.type) + 31*hash(self.id)

    def __eq__(self, other):
        return isinstance(other, BaseEntityKey) and self.type == other.type and self.id == other.id

    def __str__(self):
        return f"{self.type}:{self.id}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"