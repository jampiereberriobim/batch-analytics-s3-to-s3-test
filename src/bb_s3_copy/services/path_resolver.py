from datetime import date

from bb_s3_copy.domain.request import S3Location
from bb_s3_copy.logger import get_logger


class PathResolver:

    def __init__(self):
        self._logger = get_logger(__name__)

    def resolve(
        self,
        location: S3Location,
        execution_date: date,
    ) -> str:
        """
        Builds the S3 prefix from the configured location.
        """

        self._logger.info(
            "Resolving path. Prefix='%s', Template='%s', Suffix='%s'.",
            location.prefix,
            location.date_template,
            location.suffix,
        )

        path = (
            location.prefix
            + self._resolve_date_template(
                location.date_template,
                execution_date,
            )
            + location.suffix
        )

        path = self._normalize(path)

        self._logger.info(
            "Resolved path: '%s'.",
            path,
        )

        return path

    def _resolve_date_template(
        self,
        template: str,
        execution_date: date,
    ) -> str:

        if not template:
            return ""

        replacements = {
            "{yyyy}": execution_date.strftime("%Y"),
            "{yy}": execution_date.strftime("%y"),
            "{MM}": execution_date.strftime("%m"),
            "{M}": str(execution_date.month),
            "{dd}": execution_date.strftime("%d"),
            "{d}": str(execution_date.day),
            "{yyyyMMdd}": execution_date.strftime("%Y%m%d"),
            "{yyyy-MM-dd}": execution_date.strftime("%Y-%m-%d"),
            "{yyyy/MM/dd}": execution_date.strftime("%Y/%m/%d"),
        }

        result = template

        for key, value in replacements.items():
            result = result.replace(key, value)

        return result

    def _normalize(
        self,
        path: str,
    ) -> str:
        """
        Removes duplicate slashes while preserving the S3 key format.
        """

        while "//" in path:
            path = path.replace("//", "/")

        return path