import textwrap

import snakemd


def readme_feature(doc: snakemd.Document) -> snakemd.Document:

    # Some Specific information

    doc.add_heading(
        text="Official Resources",
        level=1,
    )

    # Logo

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent(
                """
                Logo Template
                """
            ),
            image={
                "rustdeskserver": "https://rustdesk.com/_astro/logo.BKb61-he.svg",
            }["rustdeskserver"],
            link="https://rustdesk.com/",
        ).__str__()
    )

    doc.add_heading(
        text="Rust Desk Server",
        level=2,
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Rust Desk Server Information:
            """
        )
    )

    doc.add_unordered_list(
        [
            "[Documentation](https://rustdesk.com/docs/en/self-host/rustdesk-server-oss/docker/)",
            "[Network Chuck](https://www.youtube.com/watch?v=EXL8mMUXs88&ab_channel=NetworkChuck)",
            "[Build Docker](https://github.com/rustdesk/rustdesk?tab=readme-ov-file#how-to-build-with-docker)",
        ]
    )

    # Todo
    #  ![not_ready.png](media/images/not_ready.png)
    #  ![ID_Relay_server.png](media/images/ID_Relay_server.png)
    #  ID server: localhost
    #  Relay server: localhost
    #  API server:
    #  Key: <landscape_id>/RustDeskServer__RustDeskServer/data/id_ed25519.pub
    #  ![ready.png](media/images/ready.png)

    # doc.add_horizontal_rule()

    return doc


if __name__ == "__main__":
    pass
