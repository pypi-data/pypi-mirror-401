import sys
import select

def read_line() -> str | None:
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.readline()

    return None


def write_line(line: str):
    sys.stdout.write(line + "\n")