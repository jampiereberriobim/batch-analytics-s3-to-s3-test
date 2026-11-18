from bb_s3_copy.domain.request import (
    S3CopyRequest,
    S3Location,
)


class RequestFactory:

    @staticmethod
    def from_config(config: dict) -> S3CopyRequest:

        return S3CopyRequest(
            source=S3Location(
                bucket=config["source_bucket"],
                prefix=config["source_prefix"],
                date_template=config["source_date_template"],
                suffix=config["source_suffix"],
            ),
            destination=S3Location(
                bucket=config["destination_bucket"],
                prefix=config["destination_prefix"],
                date_template=config["destination_date_template"],
                suffix=config["destination_suffix"],
            ),
            include_pattern=config.get("include_pattern"),
            exclude_pattern=config.get("exclude_pattern"),
            recursive=config.get("recursive", True),
            preserve_directory_structure=config.get(
                "preserve_directory_structure",
                True,
            ),
            delete_source=config.get("delete_source", False),
            fail_if_not_found=config.get(
                "fail_if_not_found",
                True,
            ),
            conflict_strategy=config.get(
                "conflict_strategy",
                "overwrite",
            ),
            flag_name_file=config.get("flag_name_file") or "",
        )
