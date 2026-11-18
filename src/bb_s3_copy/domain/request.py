from dataclasses import dataclass


@dataclass(slots=True)
class S3Location:
    bucket: str
    prefix: str
    date_template: str = ""
    suffix: str = ""


@dataclass(slots=True)
class S3CopyRequest:
    source: S3Location
    destination: S3Location

    include_pattern: str | None = None
    exclude_pattern: str | None = None

    recursive: bool = True
    preserve_directory_structure: bool = True
    delete_source: bool = False
    fail_if_not_found: bool = True
    conflict_strategy: str = "overwrite"
    flag_name_file: str = ""
