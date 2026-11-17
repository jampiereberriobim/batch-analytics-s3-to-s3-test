import time

from bb_s3_copy.adapters.s3_client import S3Client
from bb_s3_copy.domain.exceptions import CopyFailedException
from bb_s3_copy.domain.models import S3Object
from bb_s3_copy.domain.request import S3CopyRequest
from bb_s3_copy.domain.result import S3CopyResult
from bb_s3_copy.logger import get_logger






class CopyService:

    def __init__(self):
        self._logger = get_logger(__name__)
        self._s3_client = S3Client()

    def copy(
        self,
        objects: list[S3Object],
        source_prefix: str,
        destination_bucket: str,
        destination_prefix: str,
        request: S3CopyRequest,
    ) -> S3CopyResult:

        self._logger.info(
            "Starting copy of %s object(s).",
            len(objects),
        )

        start = time.perf_counter()

        copied_objects = 0
        copied_bytes = 0
        skipped_objects = 0
        deleted_objects = 0
        failed_objects = 0

        # Fragmento principal de CopyService
        for obj in objects:
            try:
                destination_key = self._build_destination_key(
                    obj.key, source_prefix, destination_prefix, request
                )

                exists = self._s3_client.object_exists(
                    bucket=destination_bucket,
                    key=destination_key,
                )

                if request.conflict_strategy == "skip" and exists:
                    skipped_objects += 1
                    continue

                if request.conflict_strategy == "fail" and exists:
                    raise CopyFailedException(
                        f"Destination object already exists: {destination_key}"
                    )

                self._s3_client.copy_object(
                    source_bucket=obj.bucket,
                    source_key=obj.key,
                    destination_bucket=destination_bucket,
                    destination_key=destination_key,
                )

                copied_objects += 1
                copied_bytes += obj.size

                if request.delete_source:
                    self._s3_client.delete_object(
                        bucket=obj.bucket,
                        key=obj.key,
                    )
                    deleted_objects += 1

            except Exception as e:
                failed_objects += 1

                self._logger.exception(
                    "Failed copying object '%s': %s",
                    obj.key,
                    str(e),
                )

        elapsed = time.perf_counter() - start

        self._logger.info(
            "Copy completed. "
            "Copied=%s Skipped=%s Failed=%s Deleted=%s Bytes=%s Elapsed=%.2fs",
            copied_objects,
            skipped_objects,
            failed_objects,
            deleted_objects,
            copied_bytes,
            elapsed,
        )

        return S3CopyResult(
            copied_objects=copied_objects,
            copied_bytes=copied_bytes,
            skipped_objects=skipped_objects,
            deleted_objects=deleted_objects,
            failed_objects=failed_objects,
            elapsed_seconds=elapsed,
        )

    def _build_destination_key(
        self,
        source_key: str,
        source_prefix: str,
        destination_prefix: str,
        request: S3CopyRequest,
    ) -> str:

        relative_key = source_key.removeprefix(
            source_prefix
        ).lstrip("/")

        if request.preserve_directory_structure:
            return (
                destination_prefix.rstrip("/")
                + "/"
                + relative_key
            )

        filename = relative_key.split("/")[-1]

        return (
            destination_prefix.rstrip("/")
            + "/"
            + filename
        )