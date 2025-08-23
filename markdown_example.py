from markdown_it import MarkdownIt

from text_sizing import print_big, supports_text_sizing_protocol, terminal_cbreak_mode

HEADING_SCALE_MAP = {
    "h1": 4,
    "h2": 3,
    "h3": 2,
}


def render_markdown(markdown: str) -> None:
    # WARNING: Quick and dirty markdown rendering for test purposes!

    parser = MarkdownIt()
    tokens = parser.parse(markdown)

    current_tag: str | None = None
    content = ""
    for token in tokens:
        if token.type.endswith("_open"):
            current_tag = token.tag
            content = ""
        elif token.type == "inline":
            content += token.content
        elif token.type.endswith("_close"):
            assert current_tag is not None
            if current_tag[0] == "h":
                scale = HEADING_SCALE_MAP.get(current_tag, 1)
                print_big(content, scale, bold=True)
                if scale == 1:
                    print()
            else:
                print(content, end="\n\n")

            current_tag = None


EXAMPLE_MARKDOWN = """
# h1 Heading

Lorem ipsum dolor sit amet

## h2 Heading

Lorem ipsum dolor sit amet

### h3 Heading

Lorem ipsum dolor sit amet

#### h4 Heading

Lorem ipsum dolor sit amet
"""


def main() -> None:
    with terminal_cbreak_mode():
        if not supports_text_sizing_protocol():
            print("Sorry, your terminal doesn't support the text sizing protocol!")
            exit(1)

        render_markdown(EXAMPLE_MARKDOWN)


if __name__ == "__main__":
    main()
