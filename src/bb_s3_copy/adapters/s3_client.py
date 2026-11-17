from typing import Any
from botocore.exceptions import ClientError
import boto3


class S3Client:

    def __init__(self):
        self._client = boto3.client("s3",verify=False)

    def list_objects(
        self,
        bucket: str,
        prefix: str,
        recursive: bool = True,
    ) -> list[dict[str, Any]]:
        """
        List objects under a prefix.
        """
        paginator = self._client.get_paginator("list_objects_v2")

        objects = []

        for page in paginator.paginate(
            Bucket=bucket,
            Prefix=prefix,
        ):
            objects.extend(page.get("Contents", []))

        return objects

    def copy_object(
        self,
        source_bucket: str,
        source_key: str,
        destination_bucket: str,
        destination_key: str,
    ) -> None:
        """
        Copy a single object.
        """
        self._client.copy_object(
            CopySource={
                "Bucket": source_bucket,
                "Key": source_key,
            },
            Bucket=destination_bucket,
            Key=destination_key,
        )

    def delete_object(
        self,
        bucket: str,
        key: str,
    ) -> None:
        """
        Delete a single object.
        """
        self._client.delete_object(
            Bucket=bucket,
            Key=key,
        )
        
    def object_exists(
        self,
        bucket: str,
        key: str,
    ) -> bool:
        """
        Check if an object exists.
        """
        try:
            self._client.head_object(
                Bucket=bucket,
                Key=key,
            )
            return True

        except ClientError as e:

            if e.response["Error"]["Code"] in (
                "404",
                "NoSuchKey",
                "NotFound",
            ):
                return False

            raise