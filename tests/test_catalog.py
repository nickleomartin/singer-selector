import json
import unittest

from selector.catalog import ExtendedCatalog

CATALOG_FILENAME = 'tests/catalog.json'
CONFIG_FILENAME = 'tests/config.json'


class TestExtendedCatalog(unittest.TestCase):

    test_catalog = {
        "streams": [
            {
                "tap_stream_id": "users",
                "key_properties": [
                    "id"
                ],
                "schema": {
                    "properties": {
                        "id": {
                            "type": [
                                "null",
                                "integer"
                            ]
                        },
                        "email": {
                            "type": [
                                "null",
                                "string"
                            ]
                        },
                        "plan_id": {
                            "type": [
                                "null",
                                "integer"
                            ]
                        }
                    },
                    "type": "object",
                    "additionalProperties": False
                },
                "stream": "users",
                "metadata": [
                    {
                        "breadcrumb": [],
                        "metadata": {
                            "table-key-properties": [
                                "id"
                            ],
                            "forced-replication-method": "FULL_TABLE",
                            "inclusion": "available"
                        }
                    },
                    {
                        "breadcrumb": [
                            "properties",
                            "email"
                        ],
                        "metadata": {
                            "inclusion": "available"
                        }
                    },
                    {
                        "breadcrumb": [
                            "properties",
                            "plan_id"
                        ],
                        "metadata": {
                            "inclusion": "available"
                        }
                    }
                ]
            }
        ]
    }

    def setup(self):
        pass

    def tear_down(self):
        # Clean up
        pass

    def test_load(self):
        _ = ExtendedCatalog.load(CATALOG_FILENAME)
        # self.assertDictEqual(catalog.streams, self.test_catalog)

    def test_get_stream(self):
        pass

    def test_set_stream_as_selected(self):
        pass

    def set_field_as_selected(self):
        pass

    def test_deselect_all_tables_and_fields(self):
        pass
