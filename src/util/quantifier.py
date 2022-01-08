import typing


class Quantifier(object):
    def check(self, key: str, entry: typing.Dict[str, typing.Any]):
        pass


class Mandatory(Quantifier):
    def __init__(self, name: str):
        self.name = name

    def check(self, key: str, entry: typing.Dict[str, typing.Any]):
        assert self.name in entry, \
            'the field "%s" is mandatory in entry "%s"' % (self.name, key)

    def __str__(self):
        return 'the field "%s" is mandatory' % self.name


class Forbidden(Quantifier):
    def __init__(self, name: str):
        self.name = name

    def check(self, key: str, entry: typing.Dict[str, typing.Any]):
        assert self.name not in entry, \
            'the field "%s" is forbidden in entry "%s"' % (self.name, key)

    def __str__(self):
        return 'the field "%s" is forbidden' % self.name


class AllOf(Quantifier):
    def __init__(self, *names: str):
        self.names = names

    def check(self, key: str, entry: typing.Dict[str, typing.Any]):
        missing = set(self.names) - set(entry.keys())

        assert len(missing) == 0, \
            'the fields "%s" are mandatory in entry "%s"' % (", ".join(missing), key)

    def __str__(self):
        return 'all of these fields "%s" are mandatory' % ", ".join(self.names)


class AtLeastOneOf(Quantifier):
    def __init__(self, *names: str):
        self.names = names

    def check(self, key: str, entry: typing.Dict[str, typing.Any]):
        assert len(set(self.names) & set(entry)) >= 1, \
            'at least one of "%s" fields are mandatory for "%s"' % (", ".join(self.names), key)

    def __str__(self):
        return 'at least one of these fields "%s" are mandatory' % ", ".join(self.names)


class MaybeOneOf(Quantifier):
    def __init__(self, *names: str):
        self.names = names

    def check(self, key: str, entry: typing.Dict[str, typing.Any]):
        assert len(set(self.names) & set(entry)) <= 1, \
            'just one of "%s" fields are allowed for "%s"' % (", ".join(self.names), key)

    def __str__(self):
        return 'just one of "%s" fields are allowed' % ", ".join(self.names)
