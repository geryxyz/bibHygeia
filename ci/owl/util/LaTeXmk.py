import subprocess
import typing

BIBFILE_NAME: str = 'all.bib'
DEMOFILE_NAME: str = 'demo.tex'


class LaTeXmk(object):
    def __init__(self):
        self._process = subprocess.run(f'latexmk -pdf -interaction=nonstopmode {DEMOFILE_NAME}', shell=True, capture_output=True)
        self.return_code = self._process.returncode
        self.output: str = self._decode_output(self._process.stdout)
        self.errput: str = self._decode_output(self._process.stderr)

        raw_sessions: typing.List[str] = self.output.split('Latexmk: ')
        self.biber_session = ''
        for session in raw_sessions:
            if session.startswith("applying rule 'biber demo'..."):
                self.biber_session = session
                break


    @staticmethod
    def _decode_output(output: bytes) -> str:
        return output.decode('utf-8', 'ignore')

    def save_logs(self):
        with open('latexmk-out.lg', 'w', encoding='utf-8', errors='ignore') as log:
            log.write(self.output)
        with open('latexmk-err.lg', 'w', encoding='utf-8', errors='ignore') as log:
            log.write(self.errput)
