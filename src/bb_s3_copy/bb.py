from datetime import date

from bb_s3_copy.domain.request import S3CopyRequest
from bb_s3_copy.domain.result import S3CopyResult
from bb_s3_copy.logger import get_logger
from bb_s3_copy.services.copy_service import CopyService
from bb_s3_copy.services.object_discovery import ObjectDiscovery
from bb_s3_copy.services.path_resolver import PathResolver
from bb_s3_copy.services.validator import S3CopyRequestValidator


class S3Copy:

    def __init__(self):
        self._logger = get_logger(__name__)

        self._validator = S3CopyRequestValidator()
        self._path_resolver = PathResolver()
        self._object_discovery = ObjectDiscovery()
        self._copy_service = CopyService()

    def execute(
        self,
        execution_date: date,
        request: S3CopyRequest,
    ) -> S3CopyResult:

        self._logger.info("Starting S3 Copy Building Block.")

        self._logger.info("Validating request.")
        self._validator.validate(request)

        self._logger.info("Resolving source prefix.")
        source_prefix = self._path_resolver.resolve(
            request.source,
            execution_date,
        )

        self._logger.info(
            "Source prefix resolved: %s",
            source_prefix,
        )

        self._logger.info("Resolving destination prefix.")
        destination_prefix = self._path_resolver.resolve(
            request.destination,
            execution_date,
        )

        self._logger.info(
            "Destination prefix resolved: %s",
            destination_prefix,
        )

        self._logger.info("Discovering source objects.")
        objects = self._object_discovery.discover(
            bucket=request.source.bucket,
            prefix=source_prefix,
            request=request,
        )

        self._logger.info(
            "Discovered %s object(s).",
            len(objects),
        )

        result = self._copy_service.copy(
            objects=objects,
            source_prefix=source_prefix,
            destination_bucket=request.destination.bucket,
            destination_prefix=destination_prefix,
            request=request,
        )

        self._logger.info(
            "S3 Copy completed successfully. "
            "Copied=%s Failed=%s Skipped=%s Deleted=%s Bytes=%s",
            result.copied_objects,
            result.failed_objects,
            result.skipped_objects,
            result.deleted_objects,
            result.copied_bytes,
        )

        return result