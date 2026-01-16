import os

import jubladb_api.client

def test_create_api_client():
    return jubladb_api.client.create(url="https://jubla.puzzle.ch",
                              api_key=os.environ["JUBLADB_API_KEY"])

TEST_SCHAR_ID = 680