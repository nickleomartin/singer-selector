import json
import logging

LOGGER = logging.getLogger(__name__)


class SchemaSelectorEntry(object):
    """Single stream entry."""

    def __init__(self,
                 stream=None,
                 key_properties=None,
                 fields=None):
        self.stream = stream
        self.key_properties = key_properties
        self.fields = fields

    def is_selected_field(self, field):
        return field in self.fields


# TODO: use map of stream-to-index instead of looping

class SchemaSelector(object):
    """Wraps JSON stream and field selection config."""

    def __init__(self, selected_streams):
        self.selected_streams = selected_streams

    @classmethod
    def load(cls, filename):
        LOGGER.info(f'Loading {filename}')
        with open(filename) as file:
            return SchemaSelector.from_dict(json.load(file))

    @classmethod
    def from_dict(cls, data):
        selected_streams = []
        for stream in data['selected-streams']:
            entry = SchemaSelectorEntry()
            entry.stream = stream.get('selected-stream')
            entry.key_properties = stream.get('key-properties')
            entry.fields = stream.get('selected-fields')
            selected_streams.append(entry)
        return SchemaSelector(selected_streams)

    def get_selected_stream_names(self):
        return [s.stream for s in self.selected_streams]

    def get_selected_fields_for_stream(self, stream):
        for selected_stream in self.selected_streams:
            if selected_stream.stream != stream:
                continue
            return selected_stream.fields

    def get_key_properties_for_stream(self, stream):
        for selected_stream in self.selected_streams:
            if selected_stream.stream != stream:
                continue
            return selected_stream.key_properties

    def is_selected_stream(self, stream):
        return stream in self.get_selected_stream_names()

    def is_selected_field_for_stream(self, stream, field):
        selected_fields = self.get_selected_fields_for_stream(stream)
        if field in selected_fields:
            return True
        return False
