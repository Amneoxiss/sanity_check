class SanityDependencyError(Exception):
    """Error in case of a of one failure of the sanity in the dependency."""


class DecodeSanityConfigError(Exception):
    """Error in case of a failure when decoding YAML Sanity config."""
