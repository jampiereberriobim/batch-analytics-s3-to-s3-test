from bb_s3_copy.domain.exceptions import InvalidConfigurationException
from bb_s3_copy.domain.request import S3CopyRequest
from bb_s3_copy.logger import get_logger


class S3CopyRequestValidator:

    VALID_CONFLICT_STRATEGIES = {
        "overwrite",
        "skip",
        "fail",
    }

    def __init__(self):
        self._logger = get_logger(__name__)

    def validate(
        self,
        request: S3CopyRequest,
    ) -> None:

        self._logger.info("Validating request.")

        if not request.source.bucket:
            raise InvalidConfigurationException(
                "Source bucket is required."
            )

        if not request.destination.bucket:
            raise InvalidConfigurationException(
                "Destination bucket is required."
            )

        if not request.source.prefix:
            raise InvalidConfigurationException(
                "Source prefix is required."
            )

        # destination.prefix may be empty when copying to the bucket root.

        if (
            request.conflict_strategy
            not in self.VALID_CONFLICT_STRATEGIES
        ):
            raise InvalidConfigurationException(
                f"Invalid conflict strategy: "
                f"{request.conflict_strategy}"
            )

        self._logger.info("Request validation completed successfully.")
