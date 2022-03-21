from src.report_generator.failure.CheckFailure import CheckFailure


class FileLineCheckFailure(CheckFailure):
    def __init__(self, file_path: str, line_number: int, message: str):
        super().__init__(message)
        self.file_path = file_path
        self.line_number = line_number

    def to_dict(self):
        return {
            "type": self.type,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "message": self.message
        }
