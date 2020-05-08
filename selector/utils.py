
def is_stream_metadata(metadata):
    return (
        isinstance(metadata, dict)
        and len(metadata.get('breadcrumb', [])) == 0
    )


def is_field_metadata(metadata):
    return (
        isinstance(metadata, dict)
        and len(metadata.get('breadcrumb', [])) > 0
    )


def get_field_from_breadcrumb(breadcrumb):
    return breadcrumb[1]
