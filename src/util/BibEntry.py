import typing


class BibEntry(object):
    def __init__(self, entry: typing.Dict[str, typing.Any], file_path: str, line_number: int):
        self._fields = entry
        self._file_path = file_path
        self._line_number = line_number

    @property
    def key(self) -> str:
        return self._fields["ID"]

    @property
    def entry_type(self) -> str:
        return self._fields["ENTRYTYPE"]

    @property
    def fields(self):
        return self._fields

    @property
    def file_path(self):
        return self._file_path

    @property
    def line_number(self):
        return self._line_number

    def __iter__(self):
        return iter(self._fields)

    def __getitem__(self, item: str) -> typing.Any:
        return self._fields.get(item, None)

    def __str__(self) -> str:
        return f"{self.entry_type}_{self.key}"

    def to_dict(self):
        return {
            "key": self.key,
            "type": self.entry_type,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "fields": [f for f in self._fields if f != "ID" and f != "ENTRYTYPE"]
        }
