import re


ERROR_RX = re.compile("# ((I[0-9]+ ?)+)$")


def extract_expected_errors(data):
    lines = data.splitlines()
    expected = []
    for line in lines:
        match = ERROR_RX.search(line)
        if match:
            expected.extend(match.group(1).split())
    return expected
