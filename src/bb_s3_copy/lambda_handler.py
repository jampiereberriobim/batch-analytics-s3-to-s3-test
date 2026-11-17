from datetime import datetime
from dataclasses import asdict
from bb_s3_copy.adapters.dynamodb_repository import DynamoDBRepository
from bb_s3_copy.logger import get_logger
from bb_s3_copy.services.execution_service import ExecutionService

logger = get_logger(__name__)

repository = DynamoDBRepository()
execution_service = ExecutionService()


def lambda_handler(event, context):

    process_name = event["process_name"]

    start_date = None
    end_date = None

    if "start_date" in event:
        start_date = datetime.strptime(
            event["start_date"],
            "%Y-%m-%d"
        ).date()

    if "end_date" in event:
        end_date = datetime.strptime(
            event["end_date"],
            "%Y-%m-%d"
        ).date()

    config = repository.get(process_name)

    results = execution_service.execute(
        config=config,
        start_date=start_date,
        end_date=end_date,
    )

    return [asdict(result) for result in results]