import os

TESTDATA_DIR = os.path.join(os.path.dirname(__file__), "testdata")
TMPOUTPUT_DIR = os.path.join(os.path.dirname(__file__), "tmpoutput")
os.makedirs(TMPOUTPUT_DIR, exist_ok=True)


def html_file(filename: str) -> str:
    return os.path.join(TESTDATA_DIR, filename)


def tmpdir() -> str:
    return TMPOUTPUT_DIR
