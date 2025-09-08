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
                """\
                Logo RustDesk
                """
            ),
            image="https://raw.githubusercontent.com/rustdesk/rustdesk/refs/heads/master/res/logo-header.svg",
            link="https://rustdesk.com/",
        ).__str__()
    )

    doc.add_heading(
        text="Rust Desk Server (OSS)",
        level=2,
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            Rust Desk Server Information:
            """
        )
    )

    doc.add_unordered_list(
        [
            "[Github](https://github.com/rustdesk/rustdesk)",
            "[RustDesk Server (OSS)](https://github.com/rustdesk/rustdesk-server/releases/latest)",
            "[RustDesk Server (Pro)](https://github.com/rustdesk/rustdesk-server-pro/releases/latest)",
            "[Documentation](https://rustdesk.com/docs/en/self-host/rustdesk-server-oss/docker/)",
            "[Tutorial/Overview (Network Chuck)](https://www.youtube.com/watch?v=EXL8mMUXs88&ab_channel=NetworkChuck)",
            "[Build Docker Image](https://github.com/rustdesk/rustdesk?tab=readme-ov-file#how-to-build-with-docker)",
        ]
    )

    doc.add_heading(
        text="RustDesk Setup",
        level=3,
    )

    doc.add_heading(
        text="Client Installation",
        level=4,
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            RustDesk Clients are available for a variety of platforms.
            Take a look at the documentation for more information:
            """
        )
    )

    doc.add_unordered_list(
        [
            "[RustDesk Client](https://rustdesk.com/docs/en/client/)",
        ]
    )

    doc.add_heading(
        text="Client Setup",
        level=4,
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            When you run RustDesk Client (aka RustDesk Desktop), you'll
            be presented with a screen similar to this one:
            """
        )
    )

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent(
                """\
                RustDesk Client Screen
                """
            ),
            image="media/images/not_ready.png",
        ).__str__()
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            If the screen shows you the message highlighted in red, saying
            **Ready, For faster connection, please set up your own server**,
            it means that you are using RustDesks proprietary Relay Server.
            So let's switch to the **OpenStudioLandscapes-RustDeskServer**
            Relay Server:
            """
        )
    )

    doc.add_ordered_list(
        [
            "Open Settings",
            "Go to Network",
            "Unlock network settings",
            "Open ID/Relay server",
        ]
    )

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent(
                """\
                RustDesk ID/Relay server
                """
            ),
            image="media/images/ID_Relay_server.png",
        ).__str__()
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            `ID server` and `Relay server` specify the host name or IP address
            the RustDesk Server is running on (this could be `localhost` in
            case the Landscape with OpenStudioLandscapes-RustDeskServer
            Feature is running on your local machine).
            """
        )
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            `API server` can be left blank as it is only relevant in
            the Pro version.
            """
        )
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            `Key` can be derived from the following local file:
            """
        )
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            **IMPORTANT: Only share the key from the file with the `.pub`
            extension with others!**
            """
        )
    )

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent(
                """\
                .landscapes/<landscape_id>/RustDeskServer__RustDeskServer/data/id_ed25519.pub
                """
            ),
            code=True,
        ).__str__()
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            It's content looks similar to this:
            """
        )
    )

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent(
                """\
                6eU9lygBsQ5JExSvipkVlAsAlcYfKFEgEgdxzNP72SE=
                """
            ),
            code=True,
        ).__str__()
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            Copy/paste the full content into the `Key` field of
            the ID/Relay server window.
            """
        )
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            Your RustDesk screen should now display a different message and
            you have successfully configured RustDesk Client to use
            your local **OpenStudioLandscapes-RustDeskServer** server.
            """
        )
    )

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent(
                """\
                RustDesk Local Relay Server Ready
                """
            ),
            image="media/images/ready.png",
        ).__str__()
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            Repeat this procedure for all your clients and you are good
            to go to connect from one client to another using your own
            RustDesk Relay Server.
            """
        )
    )

    # doc.add_horizontal_rule()

    return doc


if __name__ == "__main__":
    pass
