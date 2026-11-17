from fnmatch import fnmatch

from bb_s3_copy.adapters.s3_client import S3Client
from bb_s3_copy.domain.models import S3Object
from bb_s3_copy.domain.request import S3CopyRequest
from bb_s3_copy.logger import get_logger


class ObjectDiscovery:

    def __init__(self):
        self._logger = get_logger(__name__)
        self._s3_client = S3Client()

    def discover(
        self,
        bucket: str,
        prefix: str,
        request: S3CopyRequest,
    ) -> list[S3Object]:

        self._logger.info(
            "Discovering objects from 's3://%s/%s'.",
            bucket,
            prefix,
        )

        objects = self._s3_client.list_objects(
            bucket=bucket,
            prefix=prefix,
            recursive=request.recursive,
        )

        self._logger.info(
            "Retrieved %s object(s) from S3.",
            len(objects),
        )

        discovered_objects = []

        for obj in objects:

            key = obj["Key"]

            if request.include_pattern:
                if not fnmatch(key, request.include_pattern):
                    continue

            if request.exclude_pattern:
                if fnmatch(key, request.exclude_pattern):
                    continue

            discovered_objects.append(
                S3Object(
                    bucket=bucket,
                    key=key,
                    size=obj["Size"],
                )
            )

        self._logger.info(
            "%s object(s) matched the configured filters.",
            len(discovered_objects),
        )

        return discovered_objects