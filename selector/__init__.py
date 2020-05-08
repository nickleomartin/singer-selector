#! /usr/bin/env python3
import logging
import argparse
from singer.catalog import write_catalog

from selector.catalog import ExtendedCatalog
from selector.schema import SchemaSelector
from selector.utils import (
    is_field_metadata,
    get_field_from_breadcrumb)

LOGGER = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--catalog',
                        help='Preliminary catalog file',
                        required=True)
    parser.add_argument('-c',
                        '--config',
                        help='Stream & field selector file',
                        required=True)

    args = parser.parse_args()
    catalog_filename = args.catalog
    selector_filename = args.config

    LOGGER.info('Beginning selection of streams and fields')

    catalog = ExtendedCatalog.load(catalog_filename)
    selector = SchemaSelector.load(selector_filename)

    for stream_idx, catalog_stream in enumerate(catalog.streams):

        if not selector.is_selected_stream(catalog_stream.stream):
            continue

        # Obtain primary key(s)
        key_properties = selector.get_key_properties_for_stream(
            catalog_stream.stream)

        # Turn on replication for stream and set key properties
        catalog.set_stream_as_selected(catalog_stream.stream,
                                       key_properties)

        for meta_idx, metadata in enumerate(catalog_stream.metadata):

            if not is_field_metadata(metadata):
                continue

            # Check if field is selected
            breadcrumb = metadata.get('breadcrumb', [])
            field = get_field_from_breadcrumb(breadcrumb)
            is_selected_field = selector.is_selected_field_for_stream(
                catalog_stream.stream, field)

            if not is_selected_field:
                continue

            catalog.set_field_as_selected(catalog_stream.stream, field)

            LOGGER.debug((f'Selecting {field} in {catalog_stream.stream}'))

    # Write to stdout
    write_catalog(catalog)

    LOGGER.info('Completed selection of streams and fields')


if __name__ == '__main__':
    main()
