import asyncio
import random

from fasthtml.common import *

from components.assets import arrow_circle_icon, github_icon
from components.chat import chat, chat_form, chat_message, chat_messages

tlink = Script(src="https://cdn.tailwindcss.com")
fasthtml_app, rt = fast_app(ws_hdr=True, hdrs=[tlink])


def title():
    return Div(
        Span("FastHTML + Modal", cls="font-bold text-6xl"),
        Span(
            Span("Get started by editing ", cls=""),
            Span(
                "app.py",
                cls="font-mono text-green-500 bg-zinc-900 px-1 py-0.5 rounded-md text-sm",
            ),
            Span(" or deploying to Modal with ", cls=""),
            Span(
                "deploy.py",
                cls="font-mono text-green-500 bg-zinc-900 px-1 py-0.5 rounded-md text-sm",
            ),
        ),
        cls="flex-1 flex flex-col items-center justify-center gap-2",
    )


def github_link():
    return A(
        github_icon(),
        Span("GitHub", cls="font-mono text-green-500 hover:text-green-400 text-sm"),
        href="https://github.com/arihanv/fasthtml-modal",
        target="_blank",
        cls="font-mono text-green-500 hover:text-green-400 flex items-center gap-1",
    )


def footer():
    return Div(
        Div(
            Div("Docs", cls="text-zinc-400 text-sm"),
            Div(
                A(
                    Span(
                        "FastHTML",
                        cls="font-mono text-green-500 group-hover:text-green-400 text-xl",
                    ),
                    Div(
                        arrow_circle_icon(),
                        cls="flex items-center justify-center text-green-500 group-hover:text-green-400 size-5 -rotate-45",
                    ),
                    href="https://fastht.ml/",
                    target="_blank",
                    cls="justify-between items-center pl-2 pr-1 flex border border-green-500 w-40 rounded-md group",
                ),
                Div(cls="w-px bg-zinc-700 h-6"),
                A(
                    Span(
                        "Modal",
                        cls="font-mono text-green-500 group-hover:text-green-400 text-xl",
                    ),
                    Div(
                        arrow_circle_icon(),
                        cls="flex items-center justify-center text-green-500 group-hover:text-green-400 size-5 -rotate-45",
                    ),
                    href="https://modal.com/docs",
                    target="_blank",
                    cls="justify-between items-center pl-2 pr-1 flex border border-green-500 w-40 rounded-md group",
                ),
                cls="flex items-center justify-start gap-2",
            ),
            cls="flex flex-col items-center gap-1",
        ),
        Div(
            Div("Source", cls="text-zinc-400 flex justify-center w-full text-sm"),
            Div(
                github_link(),
            ),
            cls="flex flex-col items-center gap-1",
        ),
        cls="flex-1 flex-col flex items-center justify-center gap-5",
    )


@rt("/")
async def get():
    cts = Div(
        title(),
        chat(),
        footer(),
        cls="flex flex-col items-center min-h-screen bg-black",
    )
    return cts


@fasthtml_app.ws("/ws")
async def ws(msg: str, send):
    chat_messages.append({"role": "user", "content": msg})

    await send(chat_form(disabled=True))
    await send(
        Div(
            chat_message(len(chat_messages) - 1), id="messages", hx_swap_oob="beforeend"
        )
    )

    message = "You typed: " + msg

    chunks = []
    while message:
        chunk_size = random.randint(4, 10)
        chunk = message[:chunk_size]
        chunks.append(chunk)
        message = message[chunk_size:]

    chat_messages.append({"role": "assistant", "content": ""})

    await send(
        Div(
            chat_message(len(chat_messages) - 1), id="messages", hx_swap_oob="beforeend"
        )
    )

    stream_response = ""
    for chunk in chunks:
        stream_response += chunk
        chat_messages[-1]["content"] += chunk
        await send(
            Span(
                chunk, id=f"msg-content-{len(chat_messages)-1}", hx_swap_oob="beforeend"
            )
        )
        await asyncio.sleep(0.2)

    await send(chat_form(disabled=False))


if __name__ == "__main__":
    serve(app="fasthtml_app")
