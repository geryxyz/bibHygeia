import abc


class CheckFailure(abc.ABC):
    """
    Abstract class for check failures.
    """

    def __init__(self, message):
        self.message = message

    @property
    def type(self):
        return self.__class__.__name__.removesuffix('CheckFailure').lower()

    @abc.abstractmethod
    def to_dict(self):
        """
        Returns a dictionary representation of the check failure.
        """

        pass
