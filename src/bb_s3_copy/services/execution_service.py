from datetime import date, timedelta

from bb_s3_copy import S3Copy
from bb_s3_copy.factories.request_factory import RequestFactory
from bb_s3_copy.logger import get_logger

logger = get_logger(__name__)

class ExecutionService:
    def __init__(self):
        self._bb = S3Copy()

    def execute(self, config, start_date=None, end_date=None):
        if start_date is None:
            offset = int(config.get("execution_offset_days", -1))
            start_date = date.today() + timedelta(days=offset)
            end_date = start_date
        elif end_date is None:
            end_date = start_date
        elif end_date < start_date:
            raise ValueError(
                "end_date must be greater than or equal to start_date."
            )

        request = RequestFactory.from_config(config)
        results = []
        current_date = start_date

        while current_date <= end_date:
            result = self._bb.execute(
                execution_date=current_date,
                request=request,
            )
            results.append(result)
            current_date += timedelta(days=1)

        return results