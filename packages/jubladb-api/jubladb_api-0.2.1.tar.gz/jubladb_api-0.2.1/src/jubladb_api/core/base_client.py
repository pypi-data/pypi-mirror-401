import abc
import dataclasses
import itertools

import requests

import jubladb_api.metamodel
from jubladb_api.core import base_entity


class BaseClient(abc.ABC):
    def __init__(self,
                 url: str,
                 headers: dict[str, str] | None = None, ):
        if url.endswith("/"):
            raise ValueError("URL must not end with a slash, use the format https://db.example.ch")
        self._url = url
        self._headers = headers or {}
        self._cache: dict[jubladb_api.metamodel.EntityName, dict[int, object]] = {}

    def _request_list(self,
                      type_: jubladb_api.metamodel.EntityName,
                      sort: list[str] | None = None,
                      include: list[str] | None = None,
                      filters: list[tuple[str, str, list[object]]] | None = None):
        meta_type = jubladb_api.metamodel.ENTITIES[type_]
        if meta_type.url == "":
            raise ValueError(f"Entity {type_} has no url defined")
        params = []
        if sort:
            params.append(("sort", ",".join(s[:-len("_asc")] if s.endswith("_asc") else "-" + s[:-len("_desc")] for s in sort)))
        if include:
            params.append(("include", ",".join(include)))
        for (field_name, filter_type, fis) in (filters or []):
            param_name = f"filter[{field_name}][{filter_type}]"
            param_value = ",".join(str(fi) for fi in fis) if isinstance(fis, list) else str(fis)
            params.append((param_name, param_value))

        current_response = self._request_get(f"{self._url}{meta_type.url}", params)
        combined_response = {
            "data": current_response.get("data", []),
            "included": current_response.get("included", []),
        }
        while "next" in current_response.get("links", {}):
            current_response = self._request_get(self._url+current_response["links"]["next"], [])
            combined_response["data"].extend(current_response.get("data", []))
            combined_response["included"].extend(current_response.get("included", []))
        return combined_response

    def _request_single_get(self,
                            type_: jubladb_api.metamodel.EntityName,
                            id_: int,
                            include: list[str] | None = None):
        meta_type = jubladb_api.metamodel.ENTITIES[type_]
        if meta_type.url == "":
            raise ValueError(f"Entity {type_} has no url defined")
        params = []
        if include:
            params.append(("include", ",".join(include)))
        return self._request_get(f"{self._url}{meta_type.url}/{id_}", params)

    def _request_get(self,
                     url: str,
                     params: list[tuple[str, str]]) -> dict:
        effective_headers = self._headers.copy()
        effective_headers["Accept"] = "application/vnd.api+json"
        res = requests.get(url=url,
                           params=params,
                           headers=effective_headers,
                           )
        return res.json()

    def _cache_add(self, entity: base_entity.BaseEntity) -> None:
        entity_key = entity.key
        self._cache.setdefault(entity_key.type, {})[entity_key.id] = entity

    def _cache_get(self, entity_key: base_entity.BaseEntityKey) -> base_entity.BaseEntity | None:
        return self._cache.get(entity_key.type, {}).get(entity_key.id)
