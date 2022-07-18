import typing
import xml.etree.ElementTree as ET
from src.util import Singleton, Hint


class HintCollector(object, metaclass=Singleton):
    def __init__(self):
        self.hints: typing.Dict[str, typing.List[Hint]] = {}

    def add_hint(self, test_id: str, hint: Hint):
        if test_id not in self.hints:
            self.hints[test_id] = []
        self.hints[test_id].append(hint)

    def get_all_hints(self):
        return self.hints

    def get_hints(self, test_id: str) -> typing.List[Hint]:
        if test_id not in self.hints:
            return []
        return self.hints[test_id]

    def write_hints_to_xml(self, file: str, run_id: str):
        with open(file, "w", encoding="utf-8") as hint_file:
            hint_file.write('<?xml version="1.0" encoding="utf-8"?>')

            testcases = ET.Element("testcases", testsuiteid=run_id)
            for test_id, hints in self.hints.items():
                testcase = ET.SubElement(testcases, "testcase", testcaseid=test_id)
                for hint in hints:
                    hint_element = ET.SubElement(testcase, "hint")
                    hint_element.set("title", hint.title)
                    hint_element.set("recommendation", hint.recommendation)
                    hint_element.set("reason", hint.reason)
                    hint_element.set("phase", hint.phase)

            hint_file.write(ET.tostring(testcases, encoding="unicode"))
