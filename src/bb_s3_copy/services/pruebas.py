# Fragmento principal de CopyService
for obj in objects:
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
