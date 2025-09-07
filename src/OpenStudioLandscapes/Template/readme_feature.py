import textwrap

import snakemd


def readme_feature(doc: snakemd.Document) -> snakemd.Document:

    # Some Specific information

    # doc.add_heading(
    #     text="Official Resources",
    #     level=1,
    # )

    # Logo

    # doc.add_paragraph(
    #     snakemd.Inline(
    #         text=textwrap.dedent(
    #             """
    #             Logo Template
    #             """
    #         ),
    #         image={
    #             "Template": "https://www.url.com/yourlogo.png",
    #         }["Template"],
    #         link="https://www.url.com",
    #     ).__str__()
    # )
    #
    # doc.add_paragraph(
    #     text=textwrap.dedent(
    #         """
    #         Official Template information.
    #         """
    #     )
    # )

    # doc.add_horizontal_rule()

    return doc


if __name__ == "__main__":
    pass
