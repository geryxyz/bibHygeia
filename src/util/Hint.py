class Hint(object):
    def __init__(self, title: str, recommendation: str, reason: str, phase: str):
        self.title: str = title
        self.recommendation: str = recommendation
        self.reason: str = reason
        self.phase: str = phase
