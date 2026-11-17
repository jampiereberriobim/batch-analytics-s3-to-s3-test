from dataclasses import dataclass


@dataclass(slots=True)
class S3Object:
    bucket: str
    key: str
    size: int