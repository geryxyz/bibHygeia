import typing


class BibEntry(object):
    def __init__(self, entry: typing.Dict[str, typing.Any], line_number: int):
        self._fields = entry
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
    def line_number(self):
        return self._line_number

    def __iter__(self):
        return iter(self._fields)

    def __getitem__(self, item: str) -> typing.Any:
        return self._fields.get(item, None)

    def __str__(self) -> str:
        return f"{self.key}_{self.entry_type}"
