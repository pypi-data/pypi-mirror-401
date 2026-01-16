# JublaDB Python API
A package with generated code to access the [Jubla DB](https://db.jubla.ch) API with Python code.

For more information, please visit [the project page](https://github.com/Jungwacht-Herisau/jubladb_python_api)

## Requirements

Python 3.10+

## Installation
### pip install

Install the latest release from [PyPI](https://pypi.org/project/jubladb-api):
```sh
pip install jubladb_api
```

Alternatively, you can install the development version directly from GitHub:

```sh
pip install git+https://github.com/Jungwacht-Herisau/jubladb_python_api.git
```

## Getting started

```python
import jubladb_api.client
import jubladb_api.metamodel

client = jubladb_api.client.create(url=jubladb_api.metamodel.API_INFO.default_server_url,
                                   api_key="xyz")

person = client.get_person(1234, include=["roles"])
print(f"Roles of {person.first_name} {person.last_name}:")
for role_key in person.roles:
    role = client.get_role(role_key)
    print(f" - {role.name}")
```
