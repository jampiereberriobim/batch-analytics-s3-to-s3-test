import os

import boto3


class DynamoDBRepository:

    def __init__(self):
        self._table_name = os.environ["TABLE_NAME"]
        self._region = os.environ["AWS_REGION"]

        dynamodb = boto3.resource(
            "dynamodb",
            region_name=self._region,verify=False
        )

        self._table = dynamodb.Table(self._table_name)

    def get(
        self,
        process_name: str,
    ) -> dict:

        response = self._table.get_item(
            Key={
                "process_name": process_name,
            }
        )

        item = response.get("Item")

        if item is None:
            raise ValueError(
                f"Process '{process_name}' not found."
            )

        return item