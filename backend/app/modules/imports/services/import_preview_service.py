from app.modules.imports.schemas import ImportPreviewResponse
from app.modules.imports.services.csv_parser_service import CSVParserService


class ImportPreviewService:
    def __init__(self, parser: CSVParserService) -> None:
        self.parser = parser

    async def preview_csv(self, csv_bytes: bytes, source_name: str) -> ImportPreviewResponse:
        result = self.parser.parse(csv_bytes, source_name)
        return ImportPreviewResponse(
            source_name=result.source_name,
            total_rows=result.total_rows,
            valid_row_count=len(result.valid_rows),
            invalid_row_count=len(result.invalid_rows),
            valid_rows=[row.to_api() for row in result.valid_rows],
            invalid_rows=result.invalid_rows,
            warnings=result.warnings,
        )
