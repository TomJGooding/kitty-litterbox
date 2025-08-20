# https://sw.kovidgoyal.net/kitty/text-sizing-protocol/

MIN_SCALE = 1
MAX_SCALE = 7

MAX_BYTES = 4096


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


def main() -> None:
    for scale in range(MIN_SCALE, MAX_SCALE + 1):
        print_big(f"x{scale}", scale)

    for scale in range(MIN_SCALE, MAX_SCALE + 1):
        print_big(f"x{scale}", scale, newline=False)


if __name__ == "__main__":
    main()
