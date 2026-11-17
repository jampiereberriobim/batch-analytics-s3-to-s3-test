import argparse
import json
import os
from dataclasses import asdict
from datetime import datetime

from bb_s3_copy.adapters.dynamodb_repository import DynamoDBRepository
from bb_s3_copy.logger import get_logger
from bb_s3_copy.services.execution_service import ExecutionService

logger = get_logger(__name__)

def parse_date(value: str | None):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="S3-to-S3 copy process for AWS Batch.",
    )
    parser.add_argument("--process-name", default=os.getenv("PROCESS_NAME"))
    parser.add_argument("--start-date", default=os.getenv("START_DATE"))
    parser.add_argument("--end-date", default=os.getenv("END_DATE"))
    return parser

def main() -> int:
    args = build_parser().parse_args()

    if not args.process_name:
        raise SystemExit(
            "process_name is required. Use --process-name or PROCESS_NAME."
        )

    repository = DynamoDBRepository()
    execution_service = ExecutionService()

    logger.info("Loading process '%s' from DynamoDB.", args.process_name)
    config = repository.get(args.process_name)

    results = execution_service.execute(
        config=config,
        start_date=parse_date(args.start_date),
        end_date=parse_date(args.end_date),
    )

    payload = [asdict(result) for result in results]
    print(json.dumps(payload, default=str))

    failed = sum(result.failed_objects for result in results)
    if failed > 0:
        logger.error("Batch completed with %s failed object(s).", failed)
        return 2

    logger.info("Batch completed successfully.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())