import logging
from singer.catalog import Catalog

from selector.utils import (
    is_stream_metadata,
    is_field_metadata,
    get_field_from_breadcrumb)


LOGGER = logging.getLogger(__name__)


class ExtendedCatalog(Catalog):
    """
    Loads, validates and then deselects all streams and
    fields in catalog.
    """

    @classmethod
    def load(cls, filename):
        LOGGER.info(f'Loading {filename}')
        catalog = super().load(filename)
        streams = cls._deselect_all_tables_and_fields(catalog)
        return ExtendedCatalog(streams)

    def get_stream(self, stream):
        for stream in self.streams:
            if stream.table_name == stream:
                yield stream
        return None

    def set_stream_as_selected(self, stream, key_properties):
        for stream_idx, catalog_stream in enumerate(self.streams):

            if catalog_stream.stream != stream:
                continue

            message = (f'stream={stream} is selected with '
                       f'key_properties={key_properties}')
            LOGGER.info(message)

            for field_idx, metadata in enumerate(catalog_stream.metadata):
                self.streams[stream_idx].metadata[
                    field_idx]['metadata']['selected'] = True

                if key_properties:
                    # Question over whether all other taps use this format?
                    self.streams[stream_idx].key_properties = key_properties

    def set_field_as_selected(self, stream, field):
        field_set = False
        for stream_idx, catalog_stream in enumerate(self.streams):

            if catalog_stream.stream != stream:
                continue

            for meta_idx, metadata in enumerate(catalog_stream.metadata):

                if not is_field_metadata(metadata):
                    continue

                breadcrumb = metadata['breadcrumb']
                metadata_field = get_field_from_breadcrumb(breadcrumb)

                if metadata_field == field:
                    self.streams[stream_idx].metadata[
                        meta_idx]['metadata']['inclusion'] = 'automatic'

                    self.streams[stream_idx].metadata[
                        meta_idx]['metadata']['selected'] = True

                    self.streams[stream_idx].metadata[
                        meta_idx]['metadata']['selected-by-default'] = True

                    field_set = True

        if not field_set:
            message = (f'Failed to select field={field} in stream={stream}')
            LOGGER.error(message)
            raise ValueError(message)

        LOGGER.debug(f'field={field} in stream={stream} is selected')

    def _deselect_all_tables_and_fields(catalog):
        """
        Reset all tables and fields to be excluded from replication.
        """

        updated_streams = []
        for stream_idx, stream in enumerate(catalog.streams):

            updated_metadata = []
            for meta_idx, metadata in enumerate(stream.metadata):

                if is_stream_metadata(metadata):
                    # Stream will not be replicated
                    metadata['metadata']['selected'] = False

                elif is_field_metadata(metadata):
                    # Field value will not be replicated
                    metadata['metadata']['inclusion'] = 'unsupported'

                else:
                    error_message = \
                        'Malformed "metadata" field in {stream_idx}'
                    LOGGER.error(error_message)
                    raise Exception(error_message)

                updated_metadata.append(metadata)

            # Replace stream's metadata with updated_metadata
            stream.metadata = updated_metadata
            updated_streams.append(stream)

        return updated_streams
