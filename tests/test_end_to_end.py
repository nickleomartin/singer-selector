import os
import subprocess
import unittest
import json

from selector import main

CATALOG_FILENAME = 'tests/catalog.json'
UPDATED_CATALOG_FILENAME = 'tests/updated_catalog.json'
CONFIG_FILENAME = 'tests/config.json'

expected_updated_catalog = {
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
                        "inclusion": "available",
                        "selected": True
                    }
                },
                {
                    "breadcrumb": [
                        "properties",
                        "email"
                    ],
                    "metadata": {
                        "inclusion": "automatic",
                        "selected": True,
                        "selected-by-default": True
                    }
                },
                {
                    "breadcrumb": [
                        "properties",
                        "plan_id"
                    ],
                    "metadata": {
                        "inclusion": "unsupported",
                        "selected": True
                    }
                }
            ]
        }
    ]
}


def run_command(command):
    """
    Run shell command.
    """
    _ = subprocess.run(command,
                       shell=True,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)


class TestCommandLineInterface(unittest.TestCase):
    """
    Invokes selector CLI to generate updated catalog.
    """

    def tearDown(self):
        os.remove('tests/updated_catalog.json')
        return super().tearDown()

    def test_selector_cli(self):
        command = (
            f'selector --config {CONFIG_FILENAME} '
            f'--catalog {CATALOG_FILENAME} '
            f'> {UPDATED_CATALOG_FILENAME}')

        run_command(command)

        with open(UPDATED_CATALOG_FILENAME) as file:
            returned_catalog = json.load(file)

        self.assertEqual(expected_updated_catalog,
                         returned_catalog)
