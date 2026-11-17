from dataclasses import dataclass


@dataclass(slots=True)
class S3CopyResult:
    copied_objects: int
    copied_bytes: int
    skipped_objects: int
    deleted_objects: int
    failed_objects: int
    elapsed_seconds: float