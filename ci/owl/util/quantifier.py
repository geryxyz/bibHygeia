import typing
import unittest


class Quantifier(object):
    def check(self, key: str, entry: typing.Dict[str, typing.Any], test: unittest.TestCase):
        return False


class Mandatory(Quantifier):
    def __init__(self, name: str):
        self.name = name

    def check(self, key: str, entry: typing.Dict[str, typing.Any], test: unittest.TestCase):
        test.assertIn(self.name, entry, f'the field "{self.name}" is mandatory in entry "{key}"')

    def __str__(self):
        return f'the field "{self.name}" is mandatory'


class Forbidden(Quantifier):
    def __init__(self, name: str):
        self.name = name

    def check(self, key: str, entry: typing.Dict[str, typing.Any], test: unittest.TestCase):
        test.assertNotIn(self.name, entry, f'the field "{self.name}" is forbidden in entry "{key}"')

    def __str__(self):
        return f'the field "{self.name}" is forbidden'


class AllOf(Quantifier):
    def __init__(self, *names: str):
        self.names = names

    def check(self, key: str, entry: typing.Dict[str, typing.Any], test: unittest.TestCase):
        for name in self.names:
            test.assertIn(name, entry, f'the field "{name}" is mandatory in entry "{key}"')
        return True

    def __str__(self):
        return f'all of these fields {", ".join(self.names)} are mandatory'


class AtLeastOneOf(Quantifier):
    def __init__(self, *names: str):
        self.names = names

    def check(self, key: str, entry: typing.Dict[str, typing.Any], test: unittest.TestCase):
        test.assertEqual(len(set(self.names) | set(entry)), 1, f'at least one of {", ".join(self.names)} fields are mandatory for {key}')

    def __str__(self):
        return f'at least one of these fields {", ".join(self.names)} are mandatory'


class MaybeOneOf(Quantifier):
    def __init__(self, *names: str):
        self.names = names

    def check(self, key: str, entry: typing.Dict[str, typing.Any], test: unittest.TestCase):
        test.assertLessEqual(len(set(self.names) | set(entry)), 1, f'just one of {", ".join(self.names)} fields are allowed for {key}')

    def __str__(self):
        return f'just one of {", ".join(self.names)} fields are allowed'
