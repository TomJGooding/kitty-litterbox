# https://sw.kovidgoyal.net/kitty/text-sizing-protocol/
import re
import sys
import termios
import tty

STDIN_FILENO = sys.stdin.fileno()

MIN_SCALE = 1
MAX_SCALE = 7

MAX_BYTES = 4096

RE_CURSOR_POSITION = re.compile(r"\x1b\[(?P<row>\d+);(?P<col>\d+)R")


def quickstart() -> None:
    print("\x1b]66;s=2;Double sized text\a\n\n", end="")
    print("\x1b]66;s=3;Triple sized text\a\n\n\n", end="")
    print("\x1b]66;n=1:d=2;Half sized text\a\n", end="")

    print("\x1b]66;n=1:d=2:w=1;Ha\a\x1b]66;n=1:d=2:w=1;lf\a\n", end="")


def print_big(text: str, scale: int, newline: bool = True) -> None:
    if scale < MIN_SCALE or scale > MAX_SCALE:
        raise ValueError(f"Scale must be between {MIN_SCALE} and {MAX_SCALE}")

    # TODO: Escape code safe UTF-8 - which mean no newlines are allowed!
    # https://sw.kovidgoyal.net/kitty/desktop-notifications/#safe-utf8

    if len(text.encode("utf-8")) > MAX_BYTES:
        # TODO: Longer strings must be broken up into multiple escape codes
        raise ValueError(f"Text must be no longer than {MAX_BYTES} bytes")

    end = "\n" * scale if newline else ""
    print(f"\x1b]66;s={scale};{text}\a", end=end)


def print_simple_superscript(text: str) -> None:
    print(f"\x1b]66;n=1:d=2;{text}\a\n", end="")


def print_compact_superscript(text: str) -> None:
    # TODO: This assumes all characters have a width of one cell
    pairs = [text[i : i + 2] for i in range(0, len(text), 2)]
    for pair in pairs:
        print(f"\x1b]66;n=1:d=2:w=1;{pair}\a", end="")
    print()


def get_cursor_position() -> tuple[int, int]:
    # Adapted from https://jwodder.github.io/kbits/posts/cursor-pos/
    print("\x1b[6n", end="", flush=True)

    resp = b""
    while not resp.endswith(b"R"):
        resp += sys.stdin.buffer.read(1)

    resp_str = resp.decode("utf-8", "surrogateescape")
    if match := RE_CURSOR_POSITION.fullmatch(resp_str):
        return (int(match["row"]), int(match["col"]))
    else:
        raise ValueError(resp_str)


def main() -> None:
    # Put the terminal in 'cbreak mode' to allow reading terminal responses
    orig_attrs = tty.setcbreak(STDIN_FILENO, termios.TCSANOW)

    print(get_cursor_position())

    # print_simple_superscript("simple superscript")
    # print_compact_superscript("compact superscript")
    #
    # for scale in range(MIN_SCALE, MAX_SCALE + 1):
    #     print_big(f"x{scale}", scale)
    #
    # for scale in range(MIN_SCALE, MAX_SCALE + 1):
    #     print_big(f"x{scale}", scale, newline=False)

    # Restore the original terminal settings
    termios.tcsetattr(STDIN_FILENO, termios.TCSANOW, orig_attrs)


if __name__ == "__main__":
    main()
